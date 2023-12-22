#!/usr/bin/env python3

"""implementation of class cache"""
import redis
import uuid
from typing import Union


class Cache:
    """Model cache system"""

    def __init__(self):
        'set up a redis instance'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''store data using random generated key'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
