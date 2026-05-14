from redis.asyncio import Redis, from_url

from app.config import settings

_redis: Redis | None = None


async def init_redis() -> None:
    global _redis
    _redis = await from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    await _redis.ping()
    print("Redis connected")


async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None


def get_redis() -> Redis:
    """
        redis: Redis = Depends(get_redis)
    """
    if _redis is None:
        raise RuntimeError("Redis not initialized — check startup logs")
    return _redis
