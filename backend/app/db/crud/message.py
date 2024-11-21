from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models.message import Message
import logging

logger = logging.getLogger(__name__)

def get_messages_by_session_id(
    db: Session, session_id: int, skip: int = 0, limit: int = 100
):
    """
    session_idに基づいてメッセージを取得します。
    """
    try:
        return (
            db.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.updated_at)
            .offset(skip)
            .limit(limit)
            .all()
        )
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving messages for session {session_id}: {str(e)}")
        return None


def get_message_by_id(db: Session, message_id: int):
    """
    session_idに基づいて単一のメッセージを取得します。
    """
    try:
        return db.query(Message).filter(Message.id == message_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving message with id {message_id}: {str(e)}")
        return None


def create_message(db: Session, session_id: int, content: str, is_user: bool):
    """
    新しいメッセージを作成します。
    """
    db_message = Message(session_id=session_id, content=content, is_user=is_user)
    try:
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating message: {str(e)}")
        return None
