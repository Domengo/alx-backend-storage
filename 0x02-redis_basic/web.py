#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def wrapper(method: callable) -> callable:
    """wrapper"""
    @wraps(method)
    def wrapped(url) -> str:
        """wrapped"""
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapped


@wrapper
def get_page(url: str) -> str:
    """get_page"""
    res = requests.get(url)
    return res.text
