from redis import asyncio as redis

from src.settings import settings


def get_redis_connection() -> redis.Redis:
    return redis.Redis(host=settings.REDIS_STORAGE_HOST, port=settings.REDIS_STORAGE_PORT, db=settings.REDIS_STORAGE_DB)
