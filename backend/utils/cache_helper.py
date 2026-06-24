"""
In-memory caching helper for frequently accessed data
"""

class SimpleCache:
    def __init__(self):
        self._cache = {}
    
    def get(self, key):
        return self._cache.get(key)
    
    def set(self, key, value):
        self._cache[key] = value
    
    def delete(self, key):
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        self._cache.clear()

# Global cache instance
_global_cache = SimpleCache()

def get_cache():
    return _global_cache

def cache_get(key):
    return get_cache().get(key)

def cache_set(key, value):
    get_cache().set(key, value)

def cache_delete(key):
    get_cache().delete(key)

def cache_clear():
    get_cache().clear()
