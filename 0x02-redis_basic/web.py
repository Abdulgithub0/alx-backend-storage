#!/usr/bin/env python3

"""The core of the function is very simple
   It uses the requests module to obtain the HTML content
   of a particular URL and returns it. It also track how many
   times a particular URL has been accessed and cache the
   result with an expiration time of 10 seconds.
"""

import requests
import redis
from typing import Callable
from functools import wraps
import time

red = redis.Redis()


def tracker(func: Callable) -> Callable:
    """create a closure environ"""
    @wraps(func)
    def wrapper(arg: str) -> str:
        """count & store given url access activities and resource"""
        resource = red.get(f'resource:{arg}')
        resource = resource.decode('utf-8') if resource else func(arg)
        red.incr(f'count:{arg}')
        red.setex(f'resource:{arg}', 10, resource)
        return resource
    return wrapper


@tracker
def get_page(url: str) -> str:
    """"Access a webserver using @param: url and return the html contents"""
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


if __name__ == '__main__':
    key = 'http://slowwly.robertomurray.co.uk'
    red.flushdb()
    get_page(key)

    print(f"Total calls -> {red.get(f'count:{key}').decode('utf-8')}\n")
    print(f"Resource -> {red.get(f'resource:{key}').decode('utf-8')}\n")
    print(f"Expire in -> {red.ttl(f'resource:{key}')} secs\n")
    get_page(key)
    time.sleep(5)

    print(f"Total calls -> {red.get(f'count:{key}').decode('utf-8')}\n")
    print(f"Resource -> {red.get(f'resource:{key}').decode('utf-8')}\n")
    print(f"Expire in -> {red.ttl(f'resource:{key}')} secs\n")

    time.sleep(5)

    print(f"Total calls -> {red.get(f'count:{key}').decode('utf-8')}\n")
    # print(f"Resource -> {red.get(f'resource:{key}').decode('utf-8')}\n")
    print(f"Expire in -> {red.ttl(f'resource:{key}')} secs\n")

    data = get_page(key)
    print(data)
    print(f"Total calls -> {red.get(f'count:{key}').decode('utf-8')}\n")
    print(f"Resource -> {red.get(f'resource:{key}').decode('utf-8')}\n")
    print(f"Expire in -> {red.ttl(f'resource:{key}')} secs\n")

    get_page(key)
    time.sleep(2)

    print(f"Total calls -> {red.get(f'count:{key}').decode('utf-8')}\n")
    print(f"Resource -> {red.get(f'resource:{key}').decode('utf-8')}\n")
    print(f"Expire in -> {red.ttl(f'resource:{key}')} secs\n")

    red.flushdb()
