# repositories/message_repository_impl.py

import logging
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from domain.repositories.message import MessageRepository
from infrastructure.database.models.message import Message

logger = logging.getLogger(__name__)


class MessageRepositoryImpl(MessageRepository):
    def get_messages_by_session_id(
        self, session_id: int, skip: int = 0, limit: int = 100
    ) -> Optional[List[Message]]:
        """
        指定された session_id に基づいてメッセージを取得します。
        """
        try:
            return (
                self._db.query(Message)
                .filter(Message.session_id == session_id)
                .order_by(Message.created_at.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.warning(
                f"Warn retrieving messages for session {session_id}: {str(e)}"
            )
            return None

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """
        指定された message_id に基づいて単一のメッセージを取得します。
        """
        try:
            return self._db.query(Message).filter(Message.id == message_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving message with id {message_id}: {str(e)}")
            return None

    def create_message(
        self, session_id: int, content: str, is_user: bool
    ) -> Optional[Message]:
        """
        新しいメッセージを作成します。
        """
        db_message = Message(session_id=session_id, content=content, is_user=is_user)
        try:
            self._db.add(db_message)
            self._db.commit()
            self._db.refresh(db_message)
            return db_message
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error creating message: {str(e)}")
            return None
