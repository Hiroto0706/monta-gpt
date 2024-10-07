from fastapi import APIRouter
from .users import router as users_router
from .chat_sessions import router as chat_sessions_router
from .messages import router as messages_router
from .auth import router as auth_router

router = APIRouter()

router.include_router(users_router)
router.include_router(chat_sessions_router)
router.include_router(messages_router)
router.include_router(auth_router)
