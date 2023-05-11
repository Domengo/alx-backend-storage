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


def call_history(method: Callable) -> Callable:
    """call history decorator"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function"""
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(result))
        return result
    return wrapper

def replay(fn: Callable) -> None:
    """replay function"""
    r = redis.Redis()
    fn_name = fn.__qualname__
    count = r.get(fn_name).decode('utf-8')
    inputs = r.lrange(fn_name + ":inputs", 0, -1)
    outputs = r.lrange(fn_name + ":outputs", 0, -1)
    print("{} was called {} times:".format(fn_name, count))
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(fn_name, i.decode('utf-8'),
                                    o.decode('utf-8')))
class Cache:
    """class Cache that initializes redis db and flush method"""
    def __init__(self):
        """initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
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
