import pytest
from app.services.cache_service import CacheService
import time

@pytest.fixture
def cache_service():
    return CacheService(ttl=1)  # 1 second TTL for testing

def test_cache_set_get(cache_service):
    cache_service.set("test_key", "test_value")
    assert cache_service.get("test_key") == "test_value"

def test_cache_expiration(cache_service):
    cache_service.set("test_key", "test_value")
    time.sleep(1.1)  # Wait for TTL to expire
    assert cache_service.get("test_key") is None

def test_cache_invalidate(cache_service):
    cache_service.set("test_key", "test_value")
    cache_service.invalidate("test_key")
    assert cache_service.get("test_key") is None

def test_cache_clear(cache_service):
    cache_service.set("key1", "value1")
    cache_service.set("key2", "value2")
    cache_service.clear()
    assert cache_service.get("key1") is None
    assert cache_service.get("key2") is None
