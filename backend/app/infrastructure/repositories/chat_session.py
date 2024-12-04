from datetime import datetime
import logging
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.cache.redis.redis_keys import (
    CACHE_DURATION_WEEK,
    get_sessions_list_key,
)
from schemas.v1.chat_session import ChatSessionResponse
from domain.repositories.chat_session import ChatSessionRepository
from infrastructure.database.models.chat_session import ChatSession
from domain.value_objects.user import UserID

logger = logging.getLogger(__name__)


class ChatSessionRepositoryImpl(ChatSessionRepository):

    def get_chat_session_by_user_id(
        self, user_id: UserID, skip: int = 0, limit: int = 100
    ) -> Optional[List[ChatSession]]:
        """
        指定された user_idに基づいてチャットセッションを取得します
        """
        cache_key = get_sessions_list_key(user_id)
        try:
            chat_sessions_data = self._redis.get(cache_key)
            chat_sessions = [ChatSessionResponse(**item) for item in chat_sessions_data]
            return chat_sessions

        except Exception as e:
            logger.info(f"Failed to get chat sessions from Redis: {str(e)}")

        try:
            chat_sessions = (
                self._db.query(ChatSession)
                .filter(
                    ChatSession.user_id == user_id,
                    ChatSession.end_time > datetime.utcnow(),
                )
                .order_by(ChatSession.start_time.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            if chat_sessions:
                # Convert ORM models to Pydantic models
                chat_sessions_response = [
                    ChatSessionResponse.from_orm(chat_session)
                    for chat_session in chat_sessions
                ]
                # Cache the result in Redis
                chat_sessions_data = [
                    chat_session.dict() for chat_session in chat_sessions_response
                ]
                try:
                    self._redis.set(
                        cache_key,
                        chat_sessions_data,
                        expiration=CACHE_DURATION_WEEK.total_seconds(),
                    )
                except Exception as e:
                    logger.warning(f"Failed to set chat sessions to Redis: {str(e)}")
                return chat_sessions_response
            else:
                return []
        except SQLAlchemyError as e:
            logger.warning(
                f"Warning retrieving chat sessions for user {user_id}: {str(e)}"
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

    # def update_chat_session_summary(
    #     self, session_id: int, summary: str
    # ) -> Optional[ChatSession]:
    #     """
    #     指定されたsession_idに基づいてチャットセッションのアップデートします
    #     """
    #     try:
    #         db_chat_session = (
    #             self._db.query(ChatSession).filter(ChatSession.id == session_id).first()
    #         )
    #         if db_chat_session:
    #             db_chat_session.summary = summary
    #             self._db.commit()
    #             self._db.refresh(db_chat_session)
    #             return db_chat_session
    #         return None
    #     except SQLAlchemyError as e:
    #         self._db.rollback()
    #         logger.error(f"Error updating chat session summary: {str(e)}")
    #         return None

    # def delete_chat_session(self, session_id: int) -> bool:
    #     """
    #     指定されたsession_idに基づいてチャットセッションのアップデートします
    #     """
    #     try:
    #         db_chat_session = (
    #             self._db.query(ChatSession).filter(ChatSession.id == session_id).first()
    #         )
    #         if db_chat_session:
    #             self._db.delete(db_chat_session)
    #             self._db.commit()
    #             return True
    #         return False
    #     except SQLAlchemyError as e:
    #         self._db.rollback()
    #         logger.error(f"Error deleting chat session: {str(e)}")
    #         return False
