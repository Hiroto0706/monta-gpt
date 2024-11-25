from typing import Generator
from infrastructure.cache.redis.redis_repository import RedisRepository
from infrastructure.cache.redis.redis_client import RedisClient


def get_redis_connection() -> RedisRepository:
    redis_client = RedisClient()
    try:
        redis_repository = RedisRepository(redis_client.get_client())
        return redis_repository
    finally:
        redis_client.close()
