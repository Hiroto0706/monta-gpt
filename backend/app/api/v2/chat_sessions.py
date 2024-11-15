import logging
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/")
async def websocket_create_chat_session(
    websocket: WebSocket,
):
    """
    WebSocketで10秒間、1秒ごとに固定メッセージを送信し、その後通信を切断するエンドポイント。

    Args:
        websocket (WebSocket): WebSocket接続オブジェクト
    """
    await websocket.accept()

    # TODO: chat_sessionを作成する処理
    session_id = 9999

    try:
        for i in range(100):  # 10秒間のループ
            # 固定のメッセージを作成
            fixed_message = {
                "session_id": session_id,
                "content": f"test:{i+1}\n",
                "created_at": datetime.utcnow().isoformat(),
            }

            # WebSocket経由でメッセージを送信
            await websocket.send_json(fixed_message)

            # 1秒間隔でメッセージを送信
            await asyncio.sleep(0.1)

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