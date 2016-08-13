__author__ = '__naresh__'

import os
import time
import asyncio
import aiohttp

POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = '/Users/nareshkumar/desktop/downloads/'


@asyncio.coroutine
def download_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    response = yield from aiohttp.request("GET", url=url)
    response = yield from response.read()
    return response


def save_image(data, file_name):
    path = os.path.join(DEST_DIR, file_name)
    with open(path, "wb") as fp:
        fp.write(data)


@asyncio.coroutine
def download_singleflag(cc):
    response = yield from download_flag(cc)
    save_image(response, "{0}.gif".format(cc.lower()))
    return "success"


def download_many():
    loop = asyncio.get_event_loop()
    to_do = [download_singleflag(cc) for cc in POP20_CC]
    wait_cor = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_cor)
    print(len(res))
    return res


def main():
    start_time = time.time()
    result = download_many()
    end_time = time.time()
    print("flags downloaded in Time : {0}".format(end_time - start_time))


if __name__ == "__main__":
    main()
