#!/usr/bin/env python3
"""class Cache"""
import redis
import uuid
from typing import Union, Any, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count calls decorator"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """class Cache that initializes redis db and flush method"""
    def __init__(self):
        """initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data in redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[Any], Any]] = None) -> Any:
        """get data from redis"""
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """get data from redis as string"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """get data from redis as int"""
        return self.get(key, int)
