# repositories/message_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.cache.redis.redis_repository import RedisRepository
from infrastructure.database.models.message import Message


class MessageRepository(ABC):
    def __init__(self, db: Session, redis: RedisRepository):
        self._db = db
        self._redis = redis

    @abstractmethod
    def get_messages_by_session_id(
        self, session_id: int, skip: int = 0, limit: int = 100
    ) -> Optional[List[Message]]:
        """
        指定された session_id に基づいてメッセージを取得します。
        """
        pass

    @abstractmethod
    def create_message(
        self, session_id: int, content: str, is_user: bool
    ) -> Optional[Message]:
        """
        新しいメッセージを作成します。
        """
        pass
