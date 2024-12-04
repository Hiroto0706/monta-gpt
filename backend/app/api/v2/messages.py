import logging

from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.orm import Session

from application.services.user_message import (
    retrieve_session_id,
    retrieve_user_message,
)
from infrastructure.database.connection import get_db_connection
from domain.services.agent_service import AgentService
from infrastructure.cache.connection import get_redis_connection
from infrastructure.cache.redis.redis_repository import RedisRepository
from utilities.access_token import verify_access_token

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/conversation")
async def websocket_conversation(
    websocket: WebSocket,
    access_token: str,
    session_id: int = 0,
    db: Session = Depends(get_db_connection),
    redis: RedisRepository = Depends(get_redis_connection),
):
    """
    Args:
        websocket (WebSocket): WebSocket接続オブジェクト
        access_token (string): 認証用のトークン
        session_id (int): ユーザーのセッションID
        db (Session): データベースセッション
        redis (Redis): Redisクライアント
    """
    agent_service = AgentService(db=db, redis=redis)

    verify_access_token(access_token)
    await websocket.accept()

    try:
        raw_message = await websocket.receive_text()
        message_content = retrieve_user_message(raw_message)
        session_id = retrieve_session_id(raw_message)

        context = await agent_service.get_conversation_history(session_id)

        # Process LLM and stream the response
        async for chunk in agent_service.process_message(
            message_content, session_id, context
        ):
            await websocket.send_json(
                {
                    "session_id": session_id,
                    "content": chunk,
                }
            )

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await websocket.send_json(
            {"error": "Unexpected error occurred", "details": str(e)}
        )

    finally:
        await websocket.close()
