#!/usr/bin/env python3
'''This module contains the definition of the class "Cache"'''
from functools import wraps
from typing import Any, Callable, Optional, Union
from uuid import uuid4

import redis


def count_calls(method: Callable[..., Any]):
    '''Decorator function to count how many times methods of the Cache class
    are called and using the same REDIS db as storage'''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function to be returned'''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    '''A class to manage caching to REDIS database'''

    def __init__(self):
        '''__init__: class instances constructor'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores <data> in Redis using randomly generated key
        and returns that key'''

        key = str(uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable[[bytes], Any] = None) -> Any:
        '''Get the value associated <key> in Redis db,
        <fn> is an optional callable which can be used convert the retrieved
        data to the desired format'''

        data = self._redis.get(key)
        if data is None or fn is None:
            return data

        return fn(data)

    def get_str(self, key: str) -> Optional[str]:
        '''Get the value associated <key> in Redis db as a string'''

        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        '''Get the value associated <key> in Redis db as an integer'''

        return self.get(key, int)
