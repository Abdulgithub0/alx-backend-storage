#!/usr/bin/env python3

"""implementation of class cache"""
import redis
import uuid
from typing import Union, Optional, Callable
import functools

anytype = Union[str, bytes, int, float]


def count_calls(fun: Callable) -> Callable:
    """create a closure"""
    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs) -> Callable:
        """track the number of time store method is call"""
        self._redis.incr(fun.__qualname__)
        return fun(self, *args, **kwargs)
    return wrapper


def call_history(func: Callable) -> Callable:
    """create a closure"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> Callable:
        """store func's domain and range for every calls to it"""
        self._redis.rpush(f'{func.__qualname__}:inputs', str(*args))
        result: anytype = func(self, *args, **kwargs)
        self._redis.rpush(f'{func.__qualname__}:outputs', str(result))
        return result
    return wrapper


class Cache:
    """Model cache system"""

    def __init__(self):
        'set up a redis instance'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: anytype) -> str:
        '''store data using random generated key'''
        self._key = str(uuid.uuid4())
        self._redis.set(self._key, data)
        return self._key

    def get(self, key: str, fn: Optional[Callable] = None) -> anytype:
        '''retrive store data from redis db'''
        data = self._redis.get(key)
        return fn(data) if fn and data else data

    def get_str(self) -> str:
        '''convert the retrive binary data to string'''
        return self.get(self._key, str)

    def get_int(self) -> int:
        '''convert the retrive binary data to int'''
        return self.get(self._key, int)