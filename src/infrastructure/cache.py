import abc


class CacheInterface(abc.ABC):
    """Interface to abstract access to data caching from the application logic"""

    @abc.abstractmethod
    def get(self, key: str):
        """Get data for a given key"""
        pass

    @abc.abstractmethod
    def set(self, key: str, data: str):
        """Set data for a given key"""
        pass

    @abc.abstractmethod
    def invalidate(self, key: str) -> None:
        """Invalidate the entry for a given key"""
        pass

    @abc.abstractmethod
    def invalidate_key_pattern(self, pattern: str):
        """Invalidate all the keys that match the pattern param"""
        pass
