import json
import logging

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


def retrieve_user_message(user_message: str):
    client_message = json.loads(user_message)
    message_content = client_message.get("message")
    if not message_content:
        logger.error("Received message does not contain 'message' field")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message format. 'message' field is required.",
        )

    return message_content


def retrieve_session_id(user_message: str):
    client_message = json.loads(user_message)
    session_id = client_message.get("session_id")
    return session_id
