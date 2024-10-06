from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db.models.user import User
import logging


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    指定されたuser_idに基づいてuserを取得します
    """
    try:
        return db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError as e:
        logging.error(f"Error retrieving user with id {user_id}: {str(e)}")
        return None


def create_user(db: Session, username: str, email: str) -> Optional[User]:
    """
    新しいユーザーを作成します
    """
    db_user = User(username=username, email=email)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        logging.error(f"Integrity error while creating user: {str(e)}")
        return None
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error creating user: {str(e)}")
        return None


def update_user(
    db: Session,
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
) -> Optional[User]:
    """
    指定されたuser_idに基づいてuserを更新します
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            if username is not None:
                db_user.username = username
            if email is not None:
                db_user.email = email
            db.commit()
            db.refresh(db_user)
            return db_user
        return None
    except IntegrityError as e:
        db.rollback()
        logging.error(f"Integrity error while updating user: {str(e)}")
        return None
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error updating user: {str(e)}")
        return None


def delete_user(db: Session, user_id: int) -> bool:
    """
    指定されたuser_idに基づいてuserを削除します
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error deleting user: {str(e)}")
        return False
