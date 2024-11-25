from datetime import timedelta

from domain.value_objects.thread import ThreadID
from domain.value_objects.user import UserID


CACHE_DURATION_WEEK = timedelta(weeks=1)
CACHE_DURATION_DAY = timedelta(days=1)
CACHE_DURATION_HALF_DAY = timedelta(hours=12)
CACHE_DURATION_HOUR = timedelta(hours=1)

CHAT_SESSIONS_LIST_KEY = "chat_sessions_list_{user_id}"
MESSAGES_LIST_KEY = "messages_list_{thread_id}"


def get_sessions_list_key(user_id: UserID):
    """特定のユーザーに紐づくセッションリストを取得するためのRedisキーを生成する関数"""
    return CHAT_SESSIONS_LIST_KEY.format(user_id=user_id.value)


def get_messages_list_key(thread_id: ThreadID):
    """特定のスレッドに紐づくメッセージリストを取得するためのRedisキーを生成する関数"""
    return MESSAGES_LIST_KEY.format(thread_id=thread_id.value)
