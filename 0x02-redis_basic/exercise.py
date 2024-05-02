#!/usr/bin/env python3
'''This module contains the definition of the class "Cache"'''
from typing import Union
from uuid import uuid4

import redis


class Cache:
    '''A class to manage caching to REDIS database'''

    def __init__(self):
        '''__init__: class instances constructor'''
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores <data> in Redis using randomly generated key
        and returns that key'''
        key = str(uuid4())

        self._redis.set(key, data)

        return key
