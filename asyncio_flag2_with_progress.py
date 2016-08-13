__author__ = '__naresh__'

import os
import asyncio
import time
import tqdm
import collections
import aiohttp
from aiohttp import web

DEFAULT_CONCURRENT_REQ = 5
MAX_CONCURRENT_REQ = 20

POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = '/Users/nareshkumar/desktop/downloads/'

Result = collections.namedtuple("Result", "status country_code")


class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code


@asyncio.coroutine
def download_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())

    response = yield from aiohttp.request("GET", url=url)
    if response.status == 200:
        image = yield from response.read()
        return image
    elif response.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(code=response.status, message=response.reason, headers=response.headers)


def save_image(data, file_name):
    path = os.path.join(DEST_DIR, file_name)
    with open(path, "wb") as fp:
        fp.write(data)


@asyncio.coroutine
def download_singleflag(cc, semaphore):
    try:
        with (yield from semaphore):
            image = yield from download_flag(cc)
    except web.HTTPNotFound:
        status = 404
        msg = 'Page Not Found'
    except Exception as exc:
        raise FetchError(cc)
    else:
        image = yield from download_flag(cc)
        #save_image(image, "{0}.gif".format(cc.lower()))
        status = 200
        msg = "Ok"

    return Result(status, cc)


@asyncio.coroutine
def download_coro():
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(DEFAULT_CONCURRENT_REQ)
    todo = [download_singleflag(cc, semaphore) for cc in POP20_CC]
    todo_iter = asyncio.as_completed(todo)
    #todo_iter = tqdm.tqdm(iterable=todo_iter, total=len(POP20_CC))

    for future in todo_iter:
        print(future)
        try:
            res = yield from future
            print(res)
        except FetchError as exc:
            print("Errrrooooooorrrr")
            status = 400
        else:
            status = res.status
        counter[status] += 1

    return counter


def download_many():
    loop = asyncio.get_event_loop()
    cor = download_coro()
    res = loop.run_until_complete(cor)
    loop.close()
    print(res)


def main():
    start_time = time.time()
    download_many()
    end_time = time.time()
    print("flags downloaded in Time : {0}".format(end_time - start_time))


if __name__ == "__main__":
    main()
