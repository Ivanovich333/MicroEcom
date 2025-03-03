import redis
import uuid
import time
from typing import Optional
from contextlib import contextmanager
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisLock:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self._locks = {}

    def _get_lock_key(self, resource_id: str) -> str:
        return f"lock:{resource_id}"

    def _get_lock_value(self) -> str:
        return str(uuid.uuid4())

    def acquire(self, resource_id: str, timeout: int = 10) -> Optional[str]:
        lock_key = self._get_lock_key(resource_id)
        lock_value = self._get_lock_value()
        
        try:
            if self.redis.set(lock_key, lock_value, ex=timeout, nx=True):
                self._locks[resource_id] = lock_value
                logger.debug(f"Acquired lock for resource {resource_id}")
                return lock_value
            logger.warning(f"Failed to acquire lock for resource {resource_id}")
            return None
        except redis.RedisError as e:
            logger.error(f"Redis error while acquiring lock for {resource_id}: {str(e)}")
            return None

    def release(self, resource_id: str) -> bool:
        lock_key = self._get_lock_key(resource_id)
        lock_value = self._locks.get(resource_id)
        
        if not lock_value:
            logger.warning(f"No lock found for resource {resource_id}")
            return False
            
        try:
            script = """
            if redis.call("get", KEYS[1]) == ARGV[1] then
                return redis.call("del", KEYS[1])
            else
                return 0
            end
            """
            
            result = self.redis.eval(script, 1, lock_key, lock_value)
            if result:
                del self._locks[resource_id]
                logger.debug(f"Released lock for resource {resource_id}")
                return True
            logger.warning(f"Failed to release lock for resource {resource_id}")
            return False
        except redis.RedisError as e:
            logger.error(f"Redis error while releasing lock for {resource_id}: {str(e)}")
            return False

    @contextmanager
    def lock(self, resource_id: str, timeout: int = 10):
        lock_value = self.acquire(resource_id, timeout)
        if not lock_value:
            raise TimeoutError(f"Could not acquire lock for resource {resource_id}")
        
        try:
            yield lock_value
        finally:
            self.release(resource_id)

redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)
lock_manager = RedisLock(redis_client) 