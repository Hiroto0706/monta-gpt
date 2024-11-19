import asyncio
import json
import logging

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import utilities.config as config
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

        llm = ChatOpenAI(
            temperature=0.7, streaming=True, openai_api_key=config.OPENAI_API_KEY
        )
        prompt = ChatPromptTemplate.from_template("User message: {message}")
        chain = prompt | llm

        res = chain.astream({"message": message_content})

        final_response = ""
        accumulated_content = ""
        chunk_size = 50

        last_send_time = asyncio.get_event_loop().time()

        async for chunk in res:
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            accumulated_content += content
            final_response += content

            current_time = asyncio.get_event_loop().time()
            if (
                len(accumulated_content) >= chunk_size
                or (current_time - last_send_time) >= 1.0
            ):
                await websocket.send_json(
                    {
                        "session_id": session_id,
                        "content": accumulated_content,
                    }
                )
                accumulated_content = ""
                last_send_time = current_time

        if accumulated_content:
            await websocket.send_json(
                {
                    "session_id": session_id,
                    "content": accumulated_content,
                }
            )

        logger.info(final_response)

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
