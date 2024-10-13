from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import httpx
import requests
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from db.connection import get_db_connection
from db.models.message import Message
from schemas.message import MessageCreateRequest, MessageResponse
import utilities.config as config

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/{thread_id}", response_model=List[MessageResponse])
async def get_messages_by_session_id(
    thread_id: int, db: Session = Depends(get_db_connection)
):
    """
    指定された `thread_id` に基づいてメッセージのリストを取得します。

    Args:
        thread_id (int): メッセージを取得するスレッドのID
        db (Session): データベースセッション

    Returns:
        List[MessageResponse]: 指定されたスレッドに含まれるメッセージのリスト

    Raises:
        HTTPException: スレッドIDに関連するメッセージが見つからない場合
    """
    try:
        messages = db.query(Message).filter(Message.session_id == thread_id).all()
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Messages not found"
            )
    except SQLAlchemyError as db_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(db_error)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return messages


@router.post("/conversation", response_model=MessageResponse)
async def send_prompt(
    message_create_request: MessageCreateRequest,
    db: Session = Depends(get_db_connection),
):
    """
    formDataから受け取った `thread_id` および `prompt` をもとに、Agentが回答を生成し、それをレスポンスとして返します。

    Args:
        message_create (MessageCreate): スレッドIDとユーザーのプロンプトを含むメッセージデータ
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
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=10.0)) as client:
        try:
            response = await client.post(
                f"{config.AGENT_URL}api/agent/",
                json={"prompt": message_create_request.prompt},
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        agent_response_content = response.json().get("response")
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
        return agent_message
    except SQLAlchemyError as db_error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(db_error)}",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
