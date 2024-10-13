from db.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def get_or_create_user(db: Session, username: str, email: str) -> User:
    """
    ユーザーを取得または作成します。

    Args:
        db (Session): データベースセッション
        username (str): ユーザー名
        email (str): メールアドレス

    Returns:
        User: 取得または作成されたユーザーオブジェクト
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.username = username
        else:
            user = User(username=username, email=email)
            db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as db_error:
        db.rollback()
        raise db_error
