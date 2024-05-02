#!/usr/bin/env python3
'''This module contains the definition of the class "Cache"'''
from functools import wraps
from typing import Any, Callable, Optional, Union
from uuid import uuid4

import redis


def count_calls(method: Callable) -> Callable:
    '''Decorator function to count how many times methods of the Cache class
    are called and using the same REDIS db as storage'''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function to be returned'''
        if isinstance(self._redis, redis.Redis):
            key = method.__qualname__
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Decorator function'''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function to be returned'''
        if isinstance(self._redis, redis.Redis):
            key = method.__qualname__
            with self._redis.pipeline() as pipe:
                pipe.rpush(key + ":inputs", str(args))
                result = method(self, *args, **kwargs)
                pipe.rpush(key + ":outputs", str(result))
                pipe.execute()
        return result
    return wrapper


def replay(fn: Callable) -> None:
    '''Displays the history of calls of a particular function'''
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    print("{} was called {} times:".format(function_name, value))
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    '''A class to manage caching to REDIS database'''

    def __init__(self):
        '''__init__: class instances constructor'''
        self._redis = redis.Redis()
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
