#!/usr/bin/env python3
'''This module contains the definition of the class "Cache"'''
from functools import wraps
from typing import Any, Callable, Optional, Union
from uuid import uuid4

from redis import Redis


def count_calls(method: Callable) -> Callable:
    '''Decorator function to count how many times methods of the Cache class
    are called and using the same REDIS db as storage'''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function to be returned'''

        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Decorator function'''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function to be returned'''
        result = method(self, *args, **kwargs)

        key = method.__qualname__
        self._redis.rpush(key + ":inputs", str(args))
        self._redis.rpush(key + ":outputs", str(result))

        return result
    return wrapper


def replay(method: Callable) -> None:
    '''Displays the history of calls of a particular Cache <method>'''
    redis = Redis()
    q_name = method.__qualname__

    count = int(redis.get(q_name))
    print(f"{q_name} was called {count} times:")

    inputs = redis.lrange(q_name + ":inputs", 0, -1)
    outputs = redis.lrange(q_name + ":outputs", 0, -1)
    for args, ret in zip(inputs, outputs):
        print(f"{q_name}(*{args.decode('utf-8')}) -> {ret.decode('utf-8')}")


class Cache:
    '''A class to manage caching to REDIS database'''

    def __init__(self):
        '''__init__: class instances constructor'''
        self._redis = Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
