#!/usr/bin/env python3
"""class Cache"""
import redis
import uuid
from typing import Union, Any, Callable


class Cache:
    """class Cache that initializes redis db and flush method"""
    def __init__(self):
        """initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data in redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
