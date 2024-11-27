import json
import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.orm import Session

from infrastructure.cache.redis.redis_keys import get_messages_list_key
from infrastructure.cache.connection import get_redis_connection
from infrastructure.cache.redis.redis_repository import RedisRepository
from services.agent import process_llm
from db.connection import get_db_connection
from db.models.message import Message
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
    verify_access_token(access_token)
    await websocket.accept()

    try:
        raw_message = await websocket.receive_text()
        client_message = json.loads(raw_message)

        message_content = client_message.get("message")
        session_id = client_message.get("session_id")
        if not message_content:
            logger.error("Received message does not contain 'message' field")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message format. 'message' field is required.",
            )

        cache_key_pattern = get_messages_list_key(session_id)
        try:
            redis.delete([cache_key_pattern])
        except Exception as e:
            logger.warning(
                f"Failed to delete cache for chat_session {session_id}: {str(e)}"
            )

        conversation_histories = (
            db.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.id.desc())
            .limit(10)
            .all()
        )

        context = [
            {
                "role": "user" if msg.is_user else "agent",
                "content": msg.content,
            }
            for msg in conversation_histories
        ]

        # Process LLM and stream the response
        async for chunk in process_llm(message_content, session_id, db, context):
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
