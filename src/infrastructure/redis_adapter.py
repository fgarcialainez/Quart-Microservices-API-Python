import redis

from infrastructure.cache import CacheInterface


class RedisAdapter(CacheInterface):
    """Redis implementation of the CacheInterface"""
    def __init__(self):
        self.client = redis.Redis(host='redis', port=6379, db=0)

    def get(self, key: str):
        """Get data for a given key"""
        return self.client.get(key)

    def set(self, key: str, data: str):
        """Set data for a given key"""
        self.client.set(key, data)

    def invalidate(self, key: str) -> None:
        """Invalidate the entry for a given key"""
        try:
            self.client.delete(key)
        except KeyError:
            return

    def invalidate_key_pattern(self, pattern: str):
        """Invalidate all the keys that match the pattern param"""
        for key in self.client.scan_iter(pattern):
            self.invalidate(key)
