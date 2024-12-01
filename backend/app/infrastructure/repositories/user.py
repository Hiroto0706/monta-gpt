import logging
from typing import Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from infrastructure.database.models.user import User
from infrastructure.repositories.user import UserRepository

logger = logging.getLogger(__name__)


class UserRepositoryImpl(UserRepository):
    def get_user(self, user_id: int) -> Optional[User]:
        """
        指定されたuser_idに基づいてユーザーを取得します。
        """
        try:
            return self._db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            logger.warning(f"Warn retrieving user with id {user_id}: {str(e)}")
            return None

    def create_user(self, username: str, email: str) -> Optional[User]:
        """
        新しいユーザーを作成します。
        """
        db_user = User(username=username, email=email)
        try:
            self._db.add(db_user)
            self._db.commit()
            self._db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self._db.rollback()
            logger.error(f"Integrity error while creating user: {str(e)}")
            return None
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            return None

    def update_user(
        self, user_id: int, username: Optional[str] = None, email: Optional[str] = None
    ) -> Optional[User]:
        """
        指定されたuser_idに基づいてユーザーを更新します。
        """
        try:
            db_user = self._db.query(User).filter(User.id == user_id).first()
            if db_user:
                if username is not None:
                    db_user.username = username
                if email is not None:
                    db_user.email = email
                self._db.commit()
                self._db.refresh(db_user)
                return db_user
            return None
        except IntegrityError as e:
            self._db.rollback()
            logger.error(f"Integrity error while updating user: {str(e)}")
            return None
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error updating user: {str(e)}")
            return None

    def delete_user(self, user_id: int) -> bool:
        """
        指定されたuser_idに基づいてユーザーを削除します。
        """
        try:
            db_user = self._db.query(User).filter(User.id == user_id).first()
            if db_user:
                self._db.delete(db_user)
                self._db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error deleting user: {str(e)}")
            return False
