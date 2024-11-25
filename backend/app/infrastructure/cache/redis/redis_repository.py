from typing import List
import json
import logging
from typing import Any

from infrastructure.cache.redis.redis_client import RedisClient

logger = logging.getLogger(__name__)


class RedisRepository:
    """Redisを用いたキャッシュ操作を提供するクラス"""

    def __init__(self, redis_client: RedisClient):
        self.client = redis_client

    def set(self, key: str, value: Any, expiration: int = None):
        """データをRedisにセットする"""
        try:
            data = json.dumps(value)
            self.client.set(key, data, ex=expiration)
        except Exception as e:
            logger.error(f"Failed to set key to Redis: {str(e)}")
            raise Exception(f"Failed to set key to Redis: {str(e)}")

    def get(self, key: str) -> Any:
        """Redisからデータを取得する"""
        try:
            data = self.client.get(key)
            if data is None:
                raise KeyError(f"{key} not found in Redis")
            return json.loads(data)
        except Exception as e:
            logger.error(f"Failed to get key from Redis: {str(e)}")
            raise Exception(f"Failed to get key from Redis: {str(e)}")

    def delete(self, patterns: List[str]):
        """指定したパターンに一致するキーを削除する"""
        errors = []
        for pattern in patterns:
            try:
                keys = self.client.scan_iter(match=pattern)
                for key in keys:
                    self.client.delete(key)
            except Exception as e:
                logger.warning(
                    f"Failed to delete key of {pattern} from Redis: {str(e)}"
                )
                errors.append(f"Failed to delete key of {pattern} from Redis: {str(e)}")
        if errors and len(errors) == len(patterns):
            raise Exception(", ".join(errors))
