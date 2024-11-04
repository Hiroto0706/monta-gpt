from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models.chat_session import ChatSession
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_chat_sessions_by_user_id(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
):
    """
    指定されたuser_idに基づいてチャットセッションを取得します。
    """
    try:
        return (
            db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(ChatSession.start_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving chat sessions for user {user_id}: {str(e)}")
        return None


def create_chat_session(db: Session, user_id: int, start_time: datetime = None):
    """
    新しいチャットセッションを作成します。
    """
    db_chat_session = ChatSession(
        user_id=user_id, start_time=start_time or datetime.utcnow()
    )
    try:
        db.add(db_chat_session)
        db.commit()
        db.refresh(db_chat_session)
        return db_chat_session
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating chat session: {str(e)}")
        return None


def update_chat_session_summary(db: Session, session_id: int, summary: str):
    """
    チャットセッションのサマリーを更新します。
    """
    try:
        db_chat_session = (
            db.query(ChatSession).filter(ChatSession.id == session_id).first()
        )
        if db_chat_session:
            db_chat_session.summary = summary
            db.commit()
            db.refresh(db_chat_session)
            return db_chat_session
        return None
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating chat session summary: {str(e)}")
        return None


def delete_chat_session(db: Session, session_id: int):
    """
    指定されたsession_idのチャットセッションを削除します。
    """
    try:
        db_chat_session = (
            db.query(ChatSession).filter(ChatSession.id == session_id).first()
        )
        if db_chat_session:
            db.delete(db_chat_session)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting chat session: {str(e)}")
        return False
