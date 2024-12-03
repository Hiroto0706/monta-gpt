import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from application.usecase.generate_google_auth_url_usecase import (
    GenerateGoogleAuthURLUseCase,
)
from application.usecase.handle_google_auth_callback_usecase import (
    HandleGoogleAuthCallbackUseCase,
)
from application.services.user import get_user_payload
from domain.services.generate_google_auth_url_service import (
    GenerateGoogleAuthURLService,
)
from domain.services.handle_google_auth_callback_usecase_service import (
    HandleGoogleAuthCallbackService,
)
from db.connection import get_db_connection
from sqlalchemy.orm import Session


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/google/login")
async def google_auth_login() -> Dict[str, str]:
    """
    Google認証用のURLを生成します。

    Returns:
        dict: Google認証ページのURL
    """
    google_auth_login_service: GenerateGoogleAuthURLUseCase = (
        GenerateGoogleAuthURLService()
    )
    return google_auth_login_service.execute()


@router.get("/google/callback")
async def google_auth_callback(
    code: str,
    db: Session = Depends(get_db_connection),
) -> RedirectResponse:
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
    google_auth_callback_service: HandleGoogleAuthCallbackUseCase = (
        HandleGoogleAuthCallbackService(db=db)
    )
    try:
        return google_auth_callback_service.execute(code)
    except Exception as e:
        logger.error(f"Failed to handle Google auth callback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/verify")
async def verify_token(
    current_user: Dict[str, Any] = Depends(get_user_payload),
):
    """
    アクセストークンより、ユーザーの認証を行う

    Args:
        current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード

    Returns:
        dict: トークンが有効であることを示すメッセージ

    Raises:
        HTTPException: 認証に失敗した場合
    """
    return {"message": "Token is valid"}
