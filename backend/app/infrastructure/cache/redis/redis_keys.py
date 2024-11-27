from datetime import timedelta

from domain.value_objects.chat_session import ChatSessionID
from domain.value_objects.user import UserID


CACHE_DURATION_WEEK = timedelta(weeks=1)
CACHE_DURATION_DAY = timedelta(days=1)
CACHE_DURATION_HALF_DAY = timedelta(hours=12)
CACHE_DURATION_HOUR = timedelta(hours=1)

CHAT_SESSIONS_LIST_KEY = "chat_sessions_list_{user_id}"
MESSAGES_LIST_KEY = "messages_list_{chat_session_id}"


def get_sessions_list_key(user_id: UserID):
    """特定のユーザーに紐づくセッションリストを取得するためのRedisキーを生成する関数"""
    return CHAT_SESSIONS_LIST_KEY.format(user_id=user_id)


def get_messages_list_key(chat_session_id: ChatSessionID):
    """特定のスレッドに紐づくメッセージリストを取得するためのRedisキーを生成する関数"""
    return MESSAGES_LIST_KEY.format(chat_session_id=chat_session_id)
