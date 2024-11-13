from fastapi import APIRouter

# from .chat_sessions_ws import router as chat_sessions_ws_router
from .messages import router as messages_router

router = APIRouter()

# router.include_router(chat_sessions_ws_router)
router.include_router(messages_router, prefix="/messages", tags=["messages"])
