from fastapi import APIRouter
from .v1.chat_sessions import router as chat_sessions_router
from .v1.messages import router as messages_router
from .v1.auth import router as auth_router

router = APIRouter()

router.include_router(chat_sessions_router)
router.include_router(messages_router)
router.include_router(auth_router)
