import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, Dict, List
import httpx
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from services.users import get_user_payload
from db.connection import get_db_connection
from db.models.message import Message
from schemas.message import MessageCreateRequest, MessageResponse
import utilities.config as config

router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@router.get("/{thread_id}", response_model=List[MessageResponse])
async def get_messages_by_session_id(
    thread_id: int,
    current_user: Dict[str, Any] = Depends(get_user_payload),
    db: Session = Depends(get_db_connection),
):
    """
    指定された `thread_id` に基づいてメッセージのリストを取得します。

    Args:
        thread_id (int): メッセージを取得するスレッドのID
        current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード
        db (Session): データベースセッション

    Returns:
        List[MessageResponse]: 指定されたスレッドに含まれるメッセージのリスト

    Raises:
        HTTPException: スレッドIDに関連するメッセージが見つからない場合
    """
    try:
        messages = (
            db.query(Message)
            .filter(Message.session_id == thread_id)
            .order_by(Message.id)
            .all()
        )
        if not messages:
            logger.info(f"No messages found for thread ID {thread_id}.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No messages found for thread ID {thread_id}.",
            )
    except SQLAlchemyError as db_error:
        logger.error(
            f"Database error while retrieving messages for thread ID {thread_id}: {str(db_error)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while retrieving messages for thread ID {thread_id}: {str(db_error)}",
        )
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while retrieving messages for thread ID {thread_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred while retrieving messages for thread ID {thread_id}: {str(e)}",
        )
    return messages


@router.post("/conversation", response_model=MessageResponse)
async def send_prompt(
    message_create_request: MessageCreateRequest,
    current_user: Dict[str, Any] = Depends(get_user_payload),
    db: Session = Depends(get_db_connection),
):
    """
    formDataから受け取った `thread_id` および `prompt` をもとに、Agentが回答を生成し、それをレスポンスとして返します。

    Args:
        message_create (MessageCreate): スレッドIDとユーザーのプロンプトを含むメッセージデータ
        current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード
        db (Session): データベースセッション

    Returns:
        MessageResponse: Agentが生成した回答のメッセージ

    Raises:
        HTTPException: データ生成中にエラーが発生した場合
    """
    user_message = Message(
        session_id=message_create_request.session_id,
        content=message_create_request.prompt,
        is_user=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    conversation_histories = (
        db.query(Message)
        .filter(Message.session_id == message_create_request.session_id)
        .order_by(Message.id.desc())
        .limit(10)
        .all()
    )
    formatted_conversation = [
        {
            "content": msg.content,
            "is_user": msg.is_user,
            "created_at": msg.created_at.isoformat(),
        }
        for msg in conversation_histories
    ]

    logger.info(
        f"Formatted conversation history for session {message_create_request.session_id}: {formatted_conversation}"
    )

    timeout = httpx.Timeout(connect=15.0, read=60.0, write=60.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(
                f"{config.AGENT_URL}agent/",
                json={
                    "prompt": message_create_request.prompt,
                    "conversation": formatted_conversation,
                },
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            logger.error(f"HTTP request error while contacting agent API: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"HTTP request error while contacting agent API: {str(e)}",
            )
        agent_response_content = response.json().get("response")
        logger.info(f"Agent response: {agent_response_content}")

        agent_message = Message(
            session_id=message_create_request.session_id,
            content=agent_response_content,
            is_user=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    try:
        db.add(user_message)
        db.add(agent_message)
        db.commit()
        db.refresh(user_message)
        db.refresh(agent_message)
        logger.info(
            f"Successfully added user and agent messages to session {message_create_request.session_id}"
        )
        return agent_message
    except SQLAlchemyError as db_error:
        db.rollback()
        logger.error(
            f"Database error while saving messages for session {message_create_request.session_id}: {str(db_error)}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while saving messages for session {message_create_request.session_id}: {str(db_error)}",
        )
    except Exception as e:
        db.rollback()
        logger.error(
            f"Unexpected error while saving messages for session {message_create_request.session_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while saving messages for session {message_create_request.session_id}: {str(e)}",
        )
