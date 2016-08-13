__author__ = '__naresh__'

import os
import time
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed

POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = '/Users/nareshkumar/desktop/downloads/'


def download_flag(cc):
    time.sleep(1)
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    response = requests.get(url=url)
    return response.content


def save_image(data, file_name):
    path = os.path.join(DEST_DIR, file_name)
    with open(path, "wb") as fp:
        fp.write(data)


def download_many(data):
    for cc in data:
        print(cc)
        response = download_flag(cc)
        save_image(response, "{0}.gif".format(cc.lower()))


def download_singleflag(cc):
    response = download_flag(cc)
    save_image(response, "{0}.gif".format(cc.lower()))
    return "success"


def download_many_concurrent(data):
    with ThreadPoolExecutor(max_workers=20) as executer:
        threads = executer.map(download_singleflag, data)

    print(list(threads))


def download_many_concurrent_without_map(data):
    to_do = []
    with ThreadPoolExecutor(max_workers=3) as executer:
        for cc in data[:5]:
            future = executer.submit(download_singleflag, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))

        results = []

        for future in as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)

        return len(results)


def main(func):
    start_time = time.time()
    result = func(POP20_CC)
    end_time = time.time()
    print("{0} flags downloaded in Time : {1}".format(result, end_time - start_time))


if __name__ == "__main__":
    main(download_many_concurrent_without_map)
