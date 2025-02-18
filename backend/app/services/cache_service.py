from typing import Dict, Any
import time

class CacheService:
    def __init__(self, ttl: int = 3600):  # 1 hour TTL by default
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._ttl = ttl

    def get(self, key: str) -> Any:
        """Get value from cache if it exists and hasn't expired"""
        if key in self._cache:
            if time.time() - self._timestamps[key] < self._ttl:
                return self._cache[key]
            else:
                # Remove expired entry
                del self._cache[key]
                del self._timestamps[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp"""
        self._cache[key] = value
        self._timestamps[key] = time.time()

    def invalidate(self, key: str) -> None:
        """Remove entry from cache"""
        if key in self._cache:
            del self._cache[key]
            del self._timestamps[key]

    def clear(self) -> None:
        """Clear all entries from cache"""
        self._cache.clear()
        self._timestamps.clear()
