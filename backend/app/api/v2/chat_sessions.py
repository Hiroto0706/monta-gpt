import logging
import asyncio
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
):
    """
    WebSocketで10秒間、1秒ごとに固定メッセージを送信し、その後通信を切断するエンドポイント。

    Args:
        websocket (WebSocket): WebSocket接続オブジェクト
    """
    token_payload = verify_access_token(access_token)
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
            user_id=token_payload.get("user_id"),
            summary=message_content,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow()
            + timedelta(days=int(config.DEFAULT_SESSION_EXPIRATION_DAY)),
        )
        db.add(new_chat_session)
        db.commit()
        db.refresh(new_chat_session)

        for i in range(100):
            fixed_message = {
                "session_id": new_chat_session.id,
                "content": f"test:{i+1}.\nsession_id:{new_chat_session.id}\n",
                "created_at": datetime.utcnow().isoformat(),
            }

            await websocket.send_json(fixed_message)
            await asyncio.sleep(0.025)

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {new_chat_session.id}")
    except json.JSONDecodeError:
        logger.error("Invalid JSON format received from client")
        await websocket.send_json({"error": "Invalid message format. Expected JSON."})
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await websocket.send_json(
            {"error": "Unexpected error occurred", "details": str(e)}
        )
    finally:
        await websocket.close()
        logger.info(f"WebSocket connection closed for session {new_chat_session.id}")
