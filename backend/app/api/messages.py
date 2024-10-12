from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from db.connection import get_db_connection
from db.models.message import Message
from schemas.message import MessageCreateRequest, MessageResponse

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
    messages = db.query(Message).filter(Message.session_id == thread_id).all()

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Messages not found"
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
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # TODO: agentにプロンプトを渡し、解凍を生成してもらう処理を追加
    agent_response_content = "This is a placeholder response from the agent."

    agent_message = Message(
        session_id=message_create_request.session_id,
        content=agent_response_content,
        is_user=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(agent_message)
    db.commit()
    db.refresh(agent_message)

    return agent_message
