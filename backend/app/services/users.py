from db.models.user import User
from sqlalchemy.orm import Session


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
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.username = username
        db.commit()
    else:
        user = User(username=username, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
