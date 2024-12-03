import logging
from typing import Any, Dict

from fastapi import HTTPException, status

from domain.value_objects.user import UserID

logger = logging.getLogger(__name__)


def get_user_id_from_dict(current_user: Dict[str, Any]) -> UserID:
    user_id = UserID(current_user.get("user_id"))
    if not user_id:
        logger.warning("Unauthorized access attempt, user_id not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access attempt, user_id not found.",
        )

    return user_id

