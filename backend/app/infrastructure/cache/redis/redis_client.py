import logging
import utilities.config as config

import redis

logger = logging.getLogger(__name__)


class RedisClient:
    """Redisクライアントを管理するクラス"""

    def __init__(self):
        self._host = config.REDIS_HOST
        self._port = config.REDIS_PORT
        self._db = config.REDIS_DB
        self._password = config.REDIS_PASSWORD
        self._client = None

    def connect(self):
        """Redisに接続"""
        try:
            self._client = redis.Redis(
                host=self._host,
                port=self._port,
                password=self._password,
                decode_responses=True,  # Unicode文字列を返すように設定
            )
            self._client.ping()
            logger.debug("Connected to Redis")
        except ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")

    def get_client(self) -> redis.Redis:
        """Redisクライアントを取得"""
        if self._client is None:
            self.connect()
        return self._client

    def close(self):
        """Redisの接続を切断する"""
        if self._client:
            self._client.connection_pool.disconnect()
            logger.debug("Redis connection closes")
