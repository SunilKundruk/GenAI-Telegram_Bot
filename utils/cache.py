"""
Query cache — avoids re-processing identical queries.
"""
import hashlib
from collections import OrderedDict
import config

class QueryCache:
    def __init__(self, max_size: int | None = None):
        self.max_size = max_size or config.CACHE_MAX_SIZE
        self._cache: OrderedDict[str, dict] = OrderedDict()

    def _hash_key(self, query: str) -> str:
        return hashlib.sha256(query.strip().lower().encode()).hexdigest()[:16]

    def get(self, query: str) -> dict | None:
        key = self._hash_key(query)
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key].copy()
        return None

    def put(self, query: str, result: dict):
        key = self._hash_key(query)
        self._cache[key] = result.copy()
        self._cache.move_to_end(key)
        while len(self._cache) > self.max_size:
            self._cache.popitem(last=False)

query_cache = QueryCache()
