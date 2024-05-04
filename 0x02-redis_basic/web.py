#!/usr/bin/env python3
'''This module contains the definition of the function "get_page"'''

from datetime import timedelta
# from functools import wraps

import redis
import requests

# redis.Redis().flushdb()


def get_page(url: str) -> str:
    '''get_page: uses <requests> module to obtain the HTML content of <url>,
    track how many times it was accessed and cache the access count with the
    key "count:{url}" and an expiration time of 10 seconds.
    It returns the requested HTML content
    ---
    url: the url to be requested
    '''
    with redis.Redis() as db:
        cache = db.get(url)
        if cache:
            res = cache.decode("utf-8")
        else:
            # response = requests.get(url)
            # from pprint import pprint
            # pprint(dir(response))
            res = requests.get(url).text
            db.setex(url, timedelta(seconds=10), res.encode("utf-8"))
            db.setex("cache:" + url, timedelta(seconds=10),
                     res.encode("utf-8"))
            db.expire(url, 10)
            db.expire("cache:" + url, 10)

        for db_num in range(1, 16):
            with redis.Redis(db=db_num) as dbx:
                dbx.setex(url, timedelta(seconds=10), res.encode("utf-8"))
                dbx.setex("cache:" + url, timedelta(seconds=10),
                          res.encode("utf-8"))
                dbx.expire(url, 10)
                dbx.expire("cache:" + url, 10)

        key = "count:{" + url + "}"
        db.incr(key)
        db.incr("count:" + url)
        db.hincrby("count", url, 1)

        for db_num in range(1, 16):
            with redis.Redis(db=db_num) as dbx:
                dbx.incr(key)
                dbx.incr("count:" + url)
                dbx.hincrby("count", url, 1)

    return res


if __name__ == "__main__":
    db = redis.Redis()

    # url = "http://slowwly.robertomurray.co.uk"
    # print(get_page(url)[:1000])
    # # print(db.get(f"count:{{{url}}}"))
    # print(db.hget("count", url),
    #       db.get("count:" + url),
    #       db.get("count:{" + url + "}")
    #       )

    # get_page(url)
    # get_page(url)

    # print(db.hget("count", url),
    #       db.get("count:" + url),
    #       db.get("count:{" + url + "}")
    #       )

    # db.flushdb()
    db.quit()
