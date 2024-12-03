import logging
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.orm import Session
from backend.app.application.services.user_message import retrieve_user_message
from backend.app.domain.services.agent_service import AgentService
from utilities.dict import get_user_id_from_dict
from infrastructure.cache.connection import get_redis_connection
from infrastructure.cache.redis.redis_repository import RedisRepository
from db.connection import get_db_connection
from utilities.access_token import verify_access_token

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
    agent_service = AgentService(db=db, redis=redis)

    token_payload = verify_access_token(access_token)
    user_id = get_user_id_from_dict(token_payload)
    await websocket.accept()

    try:
        raw_message = await websocket.receive_text()
        message_content = retrieve_user_message(raw_message)

        # AgentServiceを使用してチャットセッションを作成
        session_id = await agent_service.create_chat_session(user_id, message_content)

        # 新規作成時はcontextがないので空にする
        async for chunk in agent_service.process_message(
            message_content, session_id, context=[]
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
