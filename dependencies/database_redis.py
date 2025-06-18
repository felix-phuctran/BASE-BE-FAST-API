from redis.asyncio import Redis

from config.env import env


def get_redis() -> Redis:
    """
    Description:
        This function is a dependency for FastAPI routes. It provides an instance of Redis client.
        The Redis client is used to interact with the Redis database for caching purposes.
    Args: None
    Returns:
        Redis: An instance of the Redis client.
    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return Redis.from_url(env.REDIS_URL, decode_responses=True)
