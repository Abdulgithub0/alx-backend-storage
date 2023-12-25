#!/usr/bin/env python3
"""implementation of class cache"""

import redis
import uuid
from typing import Union, Optional, Callable, List, Dict
import functools

anytype = Union[str, bytes, int, float]


def count_calls(fun: Callable) -> Callable:
    """create a closure"""
    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs) -> str:
        """track the number of time cache.store method is call"""
        self._redis.incr(fun.__qualname__)
        return fun(self, *args, **kwargs)
    return wrapper


def call_history(func: Callable) -> Callable:
    """create a closure"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> str:
        """store func's domain and range for every calls to it"""
        self._redis.rpush(f'{func.__qualname__}:inputs', str(args))
        result: str = str(func(self, *args, **kwargs))
        self._redis.rpush(f'{func.__qualname__}:outputs', str(result))
        return result
    return wrapper


def replay(func: Callable) -> None:
    """display number of calls, inputs, and outputs to func"""
    if not func:
        return None
    key = func.__qualname__
    r = redis.Redis()
    count = r.get(key).decode('utf-8')
    inputs = r.lrange(f'{key}:inputs', 0, -1)
    outputs = r.lrange(f'{key}:outputs', 0, -1)
    loop_len = len(outputs)
    print(f'{key} was called {count} times:')
    for ins, outs in zip(inputs, outputs):
        print(f"{key}(*{ins.decode('utf-8')}) -> {outs.decode('utf-8')}")


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

    def get_str(self, data: bytes) -> str:
        '''convert the retrieve binary data to string'''
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        '''convert the retrieve binary data to int'''
        try:
            data = int(data.decode('utf-8'))
        except Exception:
            pass
        return data
