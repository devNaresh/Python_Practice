__author__ = '__naresh__'

import asyncio
import itertools
import sys


@asyncio.coroutine
def spin(msg):
    """
    To cancel execution of spin we need to give control back
    to event loop. 'yield' or 'yield from' statement will give control
    back to event loop.

    """
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        try:
            status = char + ' ' + msg
            print(status)
            write('\x08' * len(status))
            yield from asyncio.sleep(.1)
            # yield
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():
    # pretend waiting a long time for I/O
    yield from asyncio.sleep(2)
    return 42


@asyncio.coroutine
def supervisor():
    """
    In this we can call spin() with 'yield from' as it is co-routine but
    the problem is you cannot control it from outside so we created a Task

    """

    spinner = asyncio.ensure_future(spin('thinking!'))
    # spinner = yield from spin('thinking!')
    print('spinner object:', spinner)
    result = yield from slow_function()
    print("*"*50)
    spinner.cancel()
    print('spinner object:', spinner)
    return result


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
