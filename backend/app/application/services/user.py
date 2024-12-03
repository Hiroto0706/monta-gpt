from typing import Any, Dict, Optional
from fastapi import HTTPException, Request, status
from jose import JWTError
from utilities.access_token import verify_access_token


async def get_user_payload(request: Request) -> Optional[Dict[str, Any]]:
    """
    access_tokenをともに対象のユーザー情報を取得します

    Args:
        token (str): アクセストークン

    Returns:
        User: 現在のユーザーオブジェクト
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found in cookies",
        )
    try:
        payload = verify_access_token(token)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
