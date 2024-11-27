from datetime import datetime, timedelta
import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from jose import jwt, JWTError
import utilities.config as config

ACCESS_TOKEN_EXPIRE_MINUTES = 30

logger = logging.getLogger(__name__)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    指定されたデータと有効期限でJWTアクセストークンを生成します。
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(
            to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
        )
        return encoded_jwt
    except JWTError as e:
        raise ValueError(f"Failed to create JWT token: {str(e)}")


def verify_access_token(token: str) -> Dict[str, Any]:
    """
    JWTトークンを検証する
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
