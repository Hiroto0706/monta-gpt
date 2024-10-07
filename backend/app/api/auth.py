from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
import requests
from pydantic import BaseModel
from services.users import get_or_create_user
from db.connection import get_db_connection
from db.models.user import User
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from utilities.access_token import create_access_token
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import utilities.config as config


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google/login")
async def google_auth_login():
    """
    Google認証用のURLを生成します。

    Returns:
        dict: Google認証ページのURL
    """
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{base_url}?{urlencode(params)}"
    return {"auth_url": url}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.get("/google/callback", response_model=TokenResponse)
async def google_auth_callback(
    code: str, db: Session = Depends(get_db_connection)
) -> TokenResponse:
    """
    Google OAuth2認証のコールバックを処理し、アクセストークンを生成します。

    Args:
        code (str): Google認証から返されたauthorization code
        db (Session): データベースセッション

    Returns:
        TokenResponse: 生成されたアクセストークンと種類を含むレスポンス

    Raises:
        HTTPException: 認証プロセス中にエラーが発生した場合
    """
    token_url: str = "https://oauth2.googleapis.com/token"
    token_data: Dict[str, str] = {
        "code": code,
        "client_id": config.GOOGLE_CLIENT_ID,
        "client_secret": config.GOOGLE_CLIENT_SECRET,
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response: requests.Response = requests.post(token_url, data=token_data)
    token_response_data: Dict[str, Any] = token_response.json()

    if "error" in token_response_data:
        raise HTTPException(status_code=400, detail=token_response_data["error"])

    id_token_jwt: str = token_response_data.get("id_token", "")

    try:
        id_info: Dict[str, Any] = id_token.verify_oauth2_token(
            id_token_jwt, google_requests.Request(), config.GOOGLE_CLIENT_ID
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ID token: {str(e)}")

    email: str = id_info.get("email", "")
    name: str = id_info.get("name", "")

    if not email or not name:
        raise HTTPException(
            status_code=400, detail="Email or name not found in ID token"
        )

    user: User = get_or_create_user(db=db, username=name, email=email)

    access_token: str = create_access_token(
        data={"sub": user.email, "username": user.username}
    )
    return TokenResponse(access_token=access_token, token_type="bearer")
