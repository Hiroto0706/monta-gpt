from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from infrastructure.database.models.user import User


class UserRepository(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        """
        指定されたuser_idに基づいてユーザーを取得します。
        """
        pass

    @abstractmethod
    def create_user(self, username: str, email: str) -> Optional[User]:
        """
        新しいユーザーを作成します。
        """
        pass

    @abstractmethod
    def update_user(
        self, user_id: int, username: Optional[str] = None, email: Optional[str] = None
    ) -> Optional[User]:
        """
        指定されたuser_idに基づいてユーザーを更新します。
        """
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        """
        指定されたuser_idに基づいてユーザーを削除します。
        """
        pass

    @abstractmethod
    def get_or_create_user(self, username: str, email: str) -> User:
        """
        ユーザーを取得または作成します。
        """
        pass
