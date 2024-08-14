import time


class Cache:
    def __init__(self, ttl=10, max_size=3):
        self.ttl = ttl
        self.max_size = max_size
        self.cache = {}

    def _clean_cache(self):
        # Remove expired cache entries
        current_time = time.time()
        keys_to_delete = [key for key, (value, expiry) in self.cache.items() if current_time > expiry]
        for key in keys_to_delete:
            del self.cache[key]

    def get(self, key):
        self._clean_cache()
        if key in self.cache:
            return self.cache[key][0]
        return None

    def set(self, key, value):
        self._clean_cache()
        if len(self.cache) >= self.max_size:
            # Remove the oldest item
            oldest_key = min(self.cache, key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        self.cache[key] = (value, time.time() + self.ttl)

    def __contains__(self, key):
        self._clean_cache()
        return key in self.cache
