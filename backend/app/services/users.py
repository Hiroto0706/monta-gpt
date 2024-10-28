from typing import Any, Dict, Optional
from fastapi import HTTPException, Request, status
from jose import JWTError
from utilities.access_token import verify_access_token
from db.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def get_or_create_user(db: Session, username: str, email: str) -> User:
    """
    ユーザーを取得または作成します。

    Args:
        db (Session): データベースセッション
        username (str): ユーザー名
        email (str): メールアドレス

    Returns:
        User: 取得または作成されたユーザーオブジェクト
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.username = username
        else:
            user = User(username=username, email=email)
            db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as db_error:
        db.rollback()
        raise db_error


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
