import datetime
import logging
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from domain.repositories.chat_session import ChatSessionRepository
from infrastructure.database.models.chat_session import ChatSession

logger = logging.getLogger(__name__)


class ChatSessionRepositoryImpl(ChatSessionRepository):

    def get_chat_session_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> Optional[List[ChatSession]]:
        """
        指定された user_idに基づいてチャットセッションを取得します
        """
        try:
            return (
                self._db.query(ChatSession)
                .filter(ChatSession.user_id == user_id)
                .order_by(ChatSession.start_time.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.warning(
                f"Warn retrieving chat sessions for user {user_id}: {str(e)}"
            )
            return None

    def create_chat_session(
        self, user_id: int, start_time: datetime = None
    ) -> Optional[ChatSession]:
        """
        新しいチャットセッションを作成します。
        """
        db_chat_session = ChatSession(
            user_id=user_id, start_time=start_time or datetime.utcnow()
        )
        try:
            self._db.add(db_chat_session)
            self._db.commit()
            self._db.refresh(db_chat_session)
            return db_chat_session
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error creating chat session: {str(e)}")
            return None

    def update_chat_session_summary(
        self, session_id: int, summary: str
    ) -> Optional[ChatSession]:
        """
        指定されたsession_idに基づいてチャットセッションのアップデートします
        """
        try:
            db_chat_session = (
                self._db.query(ChatSession).filter(ChatSession.id == session_id).first()
            )
            if db_chat_session:
                db_chat_session.summary = summary
                self._db.commit()
                self._db.refresh(db_chat_session)
                return db_chat_session
            return None
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error updating chat session summary: {str(e)}")
            return None

    def delete_chat_session(self, session_id: int) -> bool:
        """
        指定されたsession_idに基づいてチャットセッションのアップデートします
        """
        try:
            db_chat_session = (
                self._db.query(ChatSession).filter(ChatSession.id == session_id).first()
            )
            if db_chat_session:
                self._db.delete(db_chat_session)
                self._db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error deleting chat session: {str(e)}")
            return False
