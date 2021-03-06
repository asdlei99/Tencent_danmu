import copy
import os
import time
from contextlib import contextmanager

import moment
import numpy as np
import requests
from PIL import Image

from conf import config
from log import error, info


@contextmanager
def checkTimes(level=3, msg=" "):
    timeStart = time.time()
    yield
    info(f"{msg}cost times: {round(time.time()-timeStart,level)}s")


def error_log(default=None, need_raise=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error(f"[{func.__name__}]: {e}")
                if need_raise:
                    raise e
                return default

        return wrapper

    return decorator


def addsucess():
    config.status["success"] += 1
    config.status["fetching"] -= 1


def addfailed():
    config.status["failed"] += 1
    config.status["fetching"] -= 1


def addtotal():
    config.status["total"] += 1


def addupdate():
    config.status["fetching"] += 1


def checkPath(path):
    return os.path.exists(path)


def initPath(path):
    if not checkPath(path):
        os.makedirs(path)


def make_chunk(datas, length=512):
    data = True
    while data:
        chunk = []
        while len(chunk) < length:
            try:
                data = next(datas)
                chunk.append(data)
            except Exception as e:
                data = None
                break
        yield chunk


@error_log()
def get_pic_array(url, path):
    resp = requests.get(url)
    info(f"GET PIC From: {url}")
    with open(path, "wb") as f:
        f.write(resp.content)
    return np.array(Image.open(path))
