import logging
import json
from datetime import datetime, timedelta
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.orm import Session
from utilities.dict import get_user_id_from_dict
from infrastructure.cache.connection import get_redis_connection
from infrastructure.cache.redis.redis_keys import get_sessions_list_key
from infrastructure.cache.redis.redis_repository import RedisRepository
from services.agent import process_llm
from db.connection import get_db_connection
from db.models.chat_session import ChatSession
from utilities.access_token import verify_access_token
import utilities.config as config

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/create")
async def websocket_create_chat_session(
    websocket: WebSocket,
    access_token: str,
    db: Session = Depends(get_db_connection),
    redis: RedisRepository = Depends(get_redis_connection),
):
    """
    Args:
        websocket (WebSocket): WebSocket接続オブジェクト
        access_token (string): 認証用のトークン
        db (Session): データベースセッション
        redis (Redis): Redisクライアント
    """
    token_payload = verify_access_token(access_token)
    user_id = get_user_id_from_dict(token_payload)
    await websocket.accept()

    try:
        raw_message = await websocket.receive_text()
        client_message = json.loads(raw_message)

        message_content = client_message.get("message")
        if not message_content:
            logger.error("Received message does not contain 'message' field")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message format. 'message' field is required.",
            )

        # chat_sessionを作成
        new_chat_session = ChatSession(
            user_id=user_id,
            summary=message_content,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow()
            + timedelta(days=int(config.DEFAULT_SESSION_EXPIRATION_DAY)),
        )
        db.add(new_chat_session)
        db.commit()
        db.refresh(new_chat_session)

        session_id = new_chat_session.id

        cache_key_pattern = get_sessions_list_key(user_id)
        try:
            redis.delete([cache_key_pattern])
        except Exception as e:
            logger.warning(f"Failed to delete cache for user {user_id}: {str(e)}")

        # Process LLM and stream the response
        async for chunk in process_llm(message_content, session_id, db):
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
