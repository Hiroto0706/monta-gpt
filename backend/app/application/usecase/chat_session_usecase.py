from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from infrastructure.cache.redis.redis_repository import RedisRepository
from infrastructure.repositories.chat_session import (
    ChatSessionRepositoryImpl,
)
from schemas.v1.chat_session import (
    ChatSessionResponse,
)


class ChatSessionUseCase(ABC):
    def __init__(self, db: Session, redis: RedisRepository):
        self._db = db
        self._redis = redis
        self.chat_session_repository = ChatSessionRepositoryImpl(
            db=self._db, redis=self._redis
        )

    @abstractmethod
    async def get_chat_history(
        self, current_user: Dict[str, Any]
    ) -> List[ChatSessionResponse]:
        """
        指定されたユーザーのチャットセッション履歴を取得します。

        Args:
            current_user (Dict[str, Any]): アクセストークンから取得したユーザーペイロード
            db (Session): データベースセッション
            redis (Redis): Redisクライアント

        Returns:
            List[ChatSessionResponse]: チャットセッションのリスト

        Raises:
            HTTPException: データ取得中にエラーが発生した場合
        """
        pass

    # @abstractmethod
    # async def create_chat_session(
    #     self,
    #     chat_session_request: ChatSessionCreateRequest,
    #     current_user: Dict[str, Any],
    # ) -> ChatSessionResponse:
    #     """
    #     チャットトップページで、初めてのプロンプトを送信した際に叩かれるAPIです。
    #     ユーザーからのプロンプトを受け取り、Agentの回答を生成し、両方をデータベースに保存します。
    #     新しいセッションが作成され、プロンプトとレスポンスが保存された状態で返されます。
    #     Agentのレスポンスに含まれるsummaryもセッションに保存されます。

    #     Args:
    #         chat_session_request (ChatSessionCreateRequest): ユーザーからの質問
    #         current_user (Dict[str, Any]): 現在ログインしているユーザーの情報
    #         db (Session): データベースセッション

    #     Returns:
    #         ChatSessionResponse: 作成されたチャットセッションの情報

    #     Raises:
    #         HTTPException: セッション作成中にエラーが発生した場合
    #     """
    #     pass
