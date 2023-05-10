#!/usr/bin/env python3
"""class Cache"""
import redis
import uuid


class Cache:
    """class Cache that initializes redis db and flush method"""
    def __init__(self):
        """initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str) -> str:
        """store data in redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
