import logging
from urllib.parse import urlencode

from application.usecase.generate_google_auth_url_usecase import (
    GenerateGoogleAuthURLUseCase,
    GoogleAuthURLResponse,
)


logger = logging.getLogger(__name__)


class GenerateGoogleAuthURLService(GenerateGoogleAuthURLUseCase):
    def execute(self) -> GoogleAuthURLResponse:
        BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": self._client_id,
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": self._redirect_uri,
            "access_type": "offline",
            "prompt": "consent",
        }

        url = f"{BASE_URL}?{urlencode(params)}"
        logger.info("Generated Google Authentication URL")
        return {"auth_url": url}
