from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from db.models.message import Message
from db.connection import get_db_connection
from db.models.chat_session import ChatSession
from schemas.chat_session import (
    ChatSessionCreateRequest,
    ChatSessionDeleteResponse,
    ChatSessionUpdate,
    ChatSessionResponse,
)
import utilities.config as config

router = APIRouter(prefix="/chat_sessions", tags=["chat_sessions"])


# TODO: user_idごとにchat_sessionsを取得するように修正
@router.get("/{user_id}", response_model=List[ChatSessionResponse])
async def get_chat_history(user_id: int, db: Session = Depends(get_db_connection)):
    """
    指定されたユーザーのチャットセッション履歴を取得します。

    Args:
        user_id (int): ユーザーのID
        db (Session): データベースセッション

    Returns:
        List[ChatSessionResponse]: チャットセッションのリスト

    Raises:
        HTTPException: データ取得中にエラーが発生した場合
    """

    # TODO: DBから取得する前にredisから取得する処理を書く
    chat_sessions = db.query(ChatSession).filter(ChatSession.user_id == user_id).all()
    return chat_sessions


# TODO: userからのプロンプトもformDataから受け取る必要あり
@router.post(
    "/", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED
)
async def create_chat_session(
    chat_session_request: ChatSessionCreateRequest,
    db: Session = Depends(get_db_connection),
):
    """
    チャットトップページで、初めてのプロンプトを送信した際に叩かれるAPIです。
    ユーザーからのプロンプトを受け取り、Agentの回答を生成し、両方をデータベースに保存します。
    新しいセッションが作成され、プロンプトとレスポンスが保存された状態で返されます。
    Agentのレスポンスに含まれるsummaryもセッションに保存されます。

    Args:
        prompt (str): ユーザーが送信した最初の質問
        user_id (int): ユーザーのID
        db (Session): データベースセッション

    Returns:
        ChatSessionResponse: 作成されたチャットセッションの情報

    Raises:
        HTTPException: セッション作成中にエラーが発生した場合
    """
    user_message = Message(
        session_id=None,
        content=chat_session_request.prompt,
        is_user=True,
        timestamp=datetime.utcnow(),
        created_at=datetime.utcnow(),
    )

    # Agentの応答を生成 (ここではモックレスポンスを使用)
    agent_response_content = "This is a placeholder response from the agent."
    summary = "This is a summary response from the agent."

    agent_message = Message(
        session_id=None,
        content=agent_response_content,
        is_user=False,
        timestamp=datetime.utcnow(),
        created_at=datetime.utcnow(),
    )

    new_chat_session = ChatSession(
        user_id=chat_session_request.user_id,
        summary=summary,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow()
        + timedelta(days=int(config.DEFAULT_SESSION_EXPIRATION_DAY)),
    )
    db.add(new_chat_session)
    db.commit()
    db.refresh(new_chat_session)

    user_message.session_id = new_chat_session.id
    agent_message.session_id = new_chat_session.id

    db.add(user_message)
    db.add(agent_message)
    db.commit()
    db.refresh(user_message)
    db.refresh(agent_message)

    # TODO: redisに追加したセッションを追加する処理

    return new_chat_session


@router.delete(
    "/{session_id}",
    response_model=ChatSessionDeleteResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_chat_session(
    session_id: int, db: Session = Depends(get_db_connection)
):
    """
    指定されたチャットセッションを削除します。

    Args:
        session_id (int): 削除対象のセッションID
        db (Session): データベースセッション

    Returns:
        ChatSessionDeleteResponse: 削除成功のメッセージを含むレスポンス

    Raises:
        HTTPException: セッションが見つからない、もしくは削除中にエラーが発生した場合
    """
    chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if chat_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
        )
    db.delete(chat_session)
    db.commit()

    # TODO: redisからも対象のセッションを削除するコードを追加する必要あり
    return {"message": "delete successfully"}


@router.put("/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session(
    session_id: int,
    chat_session_update: ChatSessionUpdate,
    db: Session = Depends(get_db_connection),
):
    """
    指定されたチャットセッションを更新します。

    Args:
        session_id (int): 更新対象のセッションID
        chat_session_update (ChatSessionUpdate): 更新する内容
        db (Session): データベースセッション

    Returns:
        ChatSessionResponse: 更新されたセッションの詳細情報

    Raises:
        HTTPException: セッションが見つからない、もしくは更新中にエラーが発生した場合
    """
    chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if chat_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
        )
    for key, value in chat_session_update.dict(exclude_unset=True).items():
        setattr(chat_session, key, value)
    chat_session.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(chat_session)

    # TODO: redisの値も更新
    return chat_session
