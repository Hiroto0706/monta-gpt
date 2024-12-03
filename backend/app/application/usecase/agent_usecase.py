from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict
from sqlalchemy.orm import Session
from backend.app.infrastructure.repositories.message import MessageRepositoryImpl
from infrastructure.cache.redis.redis_repository import RedisRepository
from infrastructure.database.models.chat_session import ChatSession
from domain.value_objects.user import UserID


class AgentUseCase(ABC):

    def __init__(self, db: Session, redis: RedisRepository):
        self._db = db
        self._redis = redis
        self.message_repository = MessageRepositoryImpl(db=self._db)

    @abstractmethod
    async def delete_cache(self, redis_key: str) -> None:
        """
        Deletes the specified cache key in Redis.
        """
        pass

    @abstractmethod
    async def create_chat_session(
        self, user_id: UserID, message_content: str
    ) -> ChatSession:
        """
        Creates a new chat session and returns its ID.
        """
        pass

    @abstractmethod
    async def get_conversation_history(
        self, session_id: int, limit: int
    ) -> List[Dict[str, str]]:
        """
        Fetches the conversation history for a given session.
        """
        pass

    @abstractmethod
    async def process_message(
        self,
        message_content: str,
        session_id: int,
        context: List[Dict[str, str]],
    ) -> AsyncGenerator[str, None]:
        """
        Processes a message and streams responses from the LLM.
        """
        pass
