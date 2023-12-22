#!/usr/bin/env python3

"""implementation of class cache"""
import redis
import uuid
from typing import Union, Optional, Callable

anytype = Union[str, bytes, int, float]


class Cache:
    """Model cache system"""

    def __init__(self):
        'set up a redis instance'''
        self._redis = redis.Redis()
        self._redis.flushdb()

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
