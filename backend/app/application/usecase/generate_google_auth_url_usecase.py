from abc import ABC, abstractmethod
from typing import TypedDict
import utilities.config as config


class GoogleAuthURLResponse(TypedDict):
    auth_url: str


class GenerateGoogleAuthURLUseCase(ABC):
    def __init__(self):
        self._client_id = config.GOOGLE_CLIENT_ID
        self._redirect_uri = config.GOOGLE_REDIRECT_URI

    @abstractmethod
    def execute(self) -> GoogleAuthURLResponse:
        """
        Google認証用のURLを生成します。
        """
        pass
