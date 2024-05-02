#!/usr/bin/env python3
'''This module contains the definition of the function "get_page"'''
from datetime import timedelta
# from functools import wraps

from redis import Redis
import requests

# redis = Redis()


def get_page(url: str) -> str:
    '''get_page: uses <requests> module to obtain the HTML content of <url>,
    track how many times it was accessed and cache the access count with the
    key "count:{url}" and an expiration time of 10 seconds.
    It returns the requested HTML content

    url: the url to be requested
    '''
    with Redis() as redis:
        cache = redis.get(url)
        if cache:
            res = cache.decode("utf-8")
        else:
            res = requests.get(url).text
            redis.setx(url, res, timedelta(seconds=10))

        key = "count:" + url
        redis.incr(key)

    return res


# redis.quit()
