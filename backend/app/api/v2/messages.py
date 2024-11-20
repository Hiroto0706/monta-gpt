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
):
    """
    WebSocketで10秒間、1秒ごとに固定メッセージを送信し、その後通信を切断するエンドポイント。

    Args:
        websocket (WebSocket): WebSocket接続オブジェクト
        access_token (string): 認証用のトークン
        session_id (int): ユーザーのセッションID
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
        async for chunk in process_llm(message_content, context):
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
        # 10秒経過後にWebSocketを切断
        await websocket.close()
        logger.info(
            f"WebSocket connection closed for session {session_id} after 10 seconds"
        )
