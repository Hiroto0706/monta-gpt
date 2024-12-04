from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.cache.redis.redis_repository import RedisRepository
from infrastructure.database.models.chat_session import ChatSession


class ChatSessionRepository(ABC):
    def __init__(self, db: Session, redis: RedisRepository):
        self._db = db
        self._redis = redis

    @abstractmethod
    def get_chat_session_by_user_id(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> Optional[List[ChatSession]]:
        """
        指定された user_idに基づいてチャットセッションを取得します
        """
        pass

    @abstractmethod
    def create_chat_session(
        self, db: Session, user_id: int, start_time: datetime = None
    ) -> Optional[ChatSession]:
        """
        新しいチャットセッションを作成します
        """
        pass
