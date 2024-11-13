from fastapi import APIRouter
from .chat_sessions import router as chat_sessions_router
from .messages import router as messages_router
from .auth import router as auth_router

router = APIRouter()


router.include_router(
    chat_sessions_router, prefix="/chat_sessions", tags=["chat_sessions"]
)
router.include_router(messages_router, prefix="/messages", tags=["messages"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
