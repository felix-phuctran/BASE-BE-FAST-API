import json
import uuid
from typing import Any, Dict, Optional

from redis.asyncio import Redis


class CacheCRUDBase:
    def __init__(self, prefix: str, expire_time: int = 3600):
        """
        Initialize RedisCRUDBase with prefix and expiration time.
        
        Args:
            prefix (str): Prefix for all Redis keys
            expire_time (int): Default expiration time in seconds (default: 3600)
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        self.prefix = prefix
        self.expire_time = expire_time

    def _get_key(self, key: str) -> str:
        """
        Generate a prefixed Redis key.
        
        Args:
            key (str): Original key
            
        Returns:
            str: Prefixed key (e.g., "prefix:key")
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        return f"{self.prefix}:{key}"
    
    def _convert_uuids_to_strings(self, data: Dict) -> Dict:
        """Convert UUID objects to strings in a dictionary."""
        result = {}
        for key, value in data.items():
            if isinstance(value, uuid.UUID):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = self._convert_uuids_to_strings(value)
            elif isinstance(value, list):
                result[key] = [
                    self._convert_uuids_to_strings(item) if isinstance(item, dict)
                    else str(item) if isinstance(item, uuid.UUID)
                    else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

    async def get(self, redis: Redis, key: str) -> Optional[Any]:
        """
        Retrieve a value from Redis.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Key to retrieve
            
        Returns:
            Optional[Any]: Decoded value if exists, None otherwise
            
        Example:
            >>> value = await crud.get(redis, "user:123")
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        value = await redis.get(self._get_key(key))
        return json.loads(value) if value else None

    async def set(
        self, 
        redis: Redis, 
        key: str, 
        value: Any, 
        expire_time: Optional[int] = None
    ) -> bool:
        """
        Set a value in Redis with optional expiration.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Key to set
            value (Any): Value to store
            expire_time (Optional[int]): Custom expiration time in seconds
            
        Returns:
            bool: True if successful
            
        Example:
            >>> success = await crud.set(redis, "user:123", {"name": "John"})
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com    
        """
        if isinstance(value, dict):
            # Convert any UUID objects to strings in the dictionary
            value = self._convert_uuids_to_strings(value)
        
        serialized = json.dumps(value)
        expiry = expire_time if expire_time is not None else self.expire_time
        return await redis.set(self._get_key(key), serialized, ex=expiry)

    async def delete(self, redis: Redis, key: str) -> bool:
        """
        Delete a key from Redis.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Key to delete
            
        Returns:
            bool: True if key was deleted, False if key didn't exist
            
        Example:
            >>> deleted = await crud.delete(redis, "user:123")
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        return bool(await redis.delete(self._get_key(key)))

    async def exists(self, redis: Redis, key: str) -> bool:
        """
        Check if a key exists in Redis.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Key to check
            
        Returns:
            bool: True if key exists, False otherwise
            
        Example:
            >>> exists = await crud.exists(redis, "user:123")
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        return bool(await redis.exists(self._get_key(key)))

    async def expire(self, redis: Redis, key: str, seconds: int) -> bool:
        """
        Set expiration time for a key.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Key to set expiration for
            seconds (int): Expiration time in seconds
            
        Returns:
            bool: True if expiration was set, False otherwise
            
        Example:
            >>> success = await crud.expire(redis, "user:123", 3600)
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        return await redis.expire(self._get_key(key), seconds)

    async def ttl(self, redis: Redis, key: str) -> int:
        """
        Get remaining time to live for a key.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Key to check TTL
            
        Returns:
            int: Remaining time in seconds, -2 if key doesn't exist, -1 if no expiry
            
        Example:
            >>> remaining = await crud.ttl(redis, "user:123")
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        return await redis.ttl(self._get_key(key))

    async def incr(self, redis: Redis, key: str) -> int:
        """
        Increment a numeric value.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Key to increment
            
        Returns:
            int: New value after increment
            
        Example:
            >>> new_value = await crud.incr(redis, "counter")
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        return await redis.incr(self._get_key(key))

    async def hset(self, redis: Redis, key: str, mapping: Dict[str, Any]) -> int:
        """
        Set multiple hash fields.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Hash key
            mapping (Dict[str, Any]): Field-value mapping to set
            
        Returns:
            int: Number of fields that were added
            
        Example:
            >>> count = await crud.hset(redis, "user:123", {"name": "John", "age": 30})
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        return await redis.hset(self._get_key(key), mapping=mapping)

    async def hget(self, redis: Redis, key: str, field: str) -> Optional[str]:
        """
        Get value of a hash field.
        
        Args:
            redis (Redis): Redis connection instance
            key (str): Hash key
            field (str): Field to get
            
        Returns:
            Optional[str]: Field value if exists, None otherwise
            
        Example:
            >>> value = await crud.hget(redis, "user:123", "name")
            
        Author:
            tranvanphuc.dev.it.2002@gmail.com
        """
        return await redis.hget(self._get_key(key), field)