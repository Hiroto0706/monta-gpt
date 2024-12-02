from abc import ABC, abstractmethod
from typing import Any
from sqlalchemy.orm import Session
from infrastructure.repositories.user import UserRepositoryImpl
import utilities.config as config


class HandleGoogleAuthCallbackUseCase(ABC):
    def __init__(self, db: Session):
        self._db = db
        self._client_id = config.GOOGLE_CLIENT_ID
        self._client_secret = config.GOOGLE_CLIENT_SECRET
        self._redirect_uri = config.GOOGLE_REDIRECT_URI
        self._user_repository = UserRepositoryImpl(self._db)

    @abstractmethod
    def execute(self, code: str) -> Any:
        """
        Google OAuth2認証のコールバックを処理し、アクセストークンを生成する。
        """
        pass
