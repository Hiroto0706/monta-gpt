import logging
from fastapi import HTTPException, status
import requests
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from application.usecase.handle_google_auth_callback_usecase import (
    HandleGoogleAuthCallbackUseCase,
)
from utilities.access_token import create_access_token
import utilities.config as config


logger = logging.getLogger(__name__)


class HandleGoogleAuthCallbackService(HandleGoogleAuthCallbackUseCase):

    def execute(self, code: str) -> RedirectResponse:
        TOKEN_URL = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "redirect_uri": self._redirect_uri,
            "grant_type": "authorization_code",
        }

        try:
            token_response = requests.post(TOKEN_URL, data=token_data)
            token_response.raise_for_status()
            token_response_data = token_response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch token from Google: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch token from Google.",
            )

        if "error" in token_response_data:
            logger.warning(f"Error in token response: {token_response_data['error']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error in token response: {token_response_data['error']}",
            )
        id_token_jwt: str = token_response_data.get("id_token", "")
        if not id_token_jwt:
            logger.error("ID token not found in token response")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID token not found in token response",
            )
        try:
            id_info = id_token.verify_oauth2_token(
                id_token_jwt,
                google_requests.Request(),
                self._client_id,
                clock_skew_in_seconds=5,  # 5sの余裕を許容
            )
        except Exception as e:
            logger.error(f"Invalid ID token: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid ID token: {str(e)}")

        email: str = id_info.get("email", "")
        name: str = id_info.get("name", "")

        if not email or not name:
            logger.error("Email or name not found in ID token")
            raise HTTPException(
                status_code=400, detail="Email or name not found in ID token"
            )

        try:
            user = self._user_repository.get_or_create_user(username=name, email=email)
            logger.info(f"User {user.email} retrieved or created successfully")
        except Exception as e:
            logger.error(f"Failed to retrieve or create user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve or create user: {str(e)}",
            )

        try:
            access_token: str = create_access_token(
                data={"sub": user.email, "username": user.username, "user_id": user.id}
            )
            logger.info(f"Access token created successfully for user {user.email}")
        except Exception as e:
            logger.error(f"Failed to create access token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create access token: {str(e)}",
            )

        if config.ENV == "prd":
            secure_cookie = True
            httponly_cookie = True
        else:
            secure_cookie = False
            httponly_cookie = False

        response = RedirectResponse(url=f"{config.DOMAIN}/new")
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=httponly_cookie,
            secure=secure_cookie,
            samesite="lax",
            max_age=3600,
        )
        logger.info(
            f"Redirecting to monta-gpt.com with secure cookie: {secure_cookie}, httponly: {httponly_cookie}"
        )
        return response
