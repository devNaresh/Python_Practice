__author__ = '__naresh__'

from collections import Iterable, namedtuple
from functools import wraps
from inspect import getgeneratorstate


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x


items = [1, 2, [3, 4, [5, 6], 7], 8]

# Produces 1 2 3 4 5 6 7 8
# for x in flatten(items):
#     print(x)
#
# items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
# for x in flatten(items):
#     print(x)

data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

Result = namedtuple("Result", "average count")


def start_generator(func):
    @wraps(func)
    def inner_fuc(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return inner_fuc


def average():
    count = 0
    sum = 0
    avg = 0
    while True:
        value = yield avg
        if value is None:
            break
        sum += value
        count += 1
        avg = sum / count
    return Result(avg, count)


@start_generator
def grouper(result_dic, key):
    while True:
        result_dic[key] = yield from average()


def main():
    result_dic = {}
    for key, values in data.items():
        group = grouper(result_dic, key)
        print("Generator State Before =", getgeneratorstate(group))
        for value in values:
            group.send(value)
        group.send(None)
        group.close()
        print("Generator State Before =", getgeneratorstate(group))
    print(result_dic)


def reader():
    """A generator that fakes a read from a file, socket, etc."""
    for i in range(4):
        yield '<< %s' % i


def reader_wrapper(g):
    # Manually iterate over data produced by reader
    # for v in g:
    #     yield v
    yield from g


if __name__ == "__main__":
    # wrap = reader_wrapper(reader())
    # for i in wrap:
    #     print(i)

    main()