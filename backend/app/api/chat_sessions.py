from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from db.connection import get_db_connection
from db.models.chat_session import ChatSession
from schemas.chat_session import (
    ChatSessionCreate,
    ChatSessionDeleteResponse,
    ChatSessionUpdate,
    ChatSessionResponse,
)
import utilities.config as config

router = APIRouter(prefix="/chat_sessions", tags=["chat_sessions"])


# チャット履歴を全て取得する GET メソッド
# TODO: user_idごとにchat_sessionsを取得するように修正
@router.get("/{user_id}", response_model=List[ChatSessionResponse])
async def get_chat_history(user_id: int, db: Session = Depends(get_db_connection)):

    # TODO: DBから取得する前にredisから取得する処理を書く
    chat_sessions = db.query(ChatSession).filter(ChatSession.user_id == user_id).all()
    return chat_sessions


# 新しいチャットセッションを作成するための POST メソッド
@router.post(
    "/", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED
)
async def create_chat_session(
    chat_session: ChatSessionCreate, db: Session = Depends(get_db_connection)
):
    # FIXME: summaryはフロントから渡ってくるものではなく、Agentが作成するものなのでここで入ったんからでも良いかも
    new_chat_session = ChatSession(
        user_id=chat_session.user_id,
        summary=chat_session.summary,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow()
        + timedelta(days=int(config.DEFAULT_SESSION_EXPIRATION_DAY)),
    )
    db.add(new_chat_session)
    db.commit()
    db.refresh(new_chat_session)

    # TODO: redisに追加したセッションを追加する処理
    return new_chat_session


# 不要なチャットセッションを削除するための DELETE メソッド
@router.delete(
    "/{session_id}",
    response_model=ChatSessionDeleteResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_chat_session(
    session_id: int, db: Session = Depends(get_db_connection)
):
    chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if chat_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
        )
    db.delete(chat_session)
    db.commit()

    # TODO: redisからも対象のセッションを削除するコードを追加する必要あり
    return {"message": "delete successfully"}


# チャットのサマリーを編集するための PUT メソッド
@router.put("/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session(
    session_id: int,
    chat_session_update: ChatSessionUpdate,
    db: Session = Depends(get_db_connection),
):
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
