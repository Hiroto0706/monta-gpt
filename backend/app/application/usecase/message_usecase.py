from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from infrastructure.cache.redis.redis_repository import RedisRepository
from infrastructure.repositories.message import MessageRepositoryImpl
from schemas.v1.message import MessageResponse


class MessageUseCase(ABC):
    def __init__(self, db: Session, redis: RedisRepository):
        self._db = db
        self._redis = redis
        self.message_repository = MessageRepositoryImpl(db=db, redis=redis)

    @abstractmethod
    async def get_messages_by_session_id(
        self, session_id: int
    ) -> List[MessageResponse]:
        """
        指定された `chat_session_id` に基づいてメッセージのリストを取得します。

        Args:
            chat_session_id (int): メッセージを取得するスレッドのID
            current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード
            redis (Redis): Redisクライアント

        Returns:
            List[MessageResponse]: 指定されたスレッドに含まれるメッセージのリスト

        Raises:
            HTTPException: スレッドIDに関連するメッセージが見つからない場合
        """
        pass
