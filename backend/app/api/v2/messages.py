import json
import logging
import asyncio
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status
from datetime import datetime

from utilities.access_token import verify_access_token

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/conversation")
async def websocket_conversation(
    websocket: WebSocket,
    access_token: str,
    session_id: int = 0,
):
    """
    WebSocketで10秒間、1秒ごとに固定メッセージを送信し、その後通信を切断するエンドポイント。

    Args:
        websocket (WebSocket): WebSocket接続オブジェクト
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

        for i in range(100):  # 10秒間のループ
            # 固定のメッセージを作成
            fixed_message = {
                "session_id": session_id,
                "content": f"conversation.\nsession_id:{session_id}\n",
                "created_at": datetime.utcnow().isoformat(),
            }

            # WebSocket経由でメッセージを送信
            await websocket.send_json(fixed_message)

            # 1秒間隔でメッセージを送信
            await asyncio.sleep(0.025)

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
