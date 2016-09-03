__author__ = '__naresh__'

import asyncio
from aiohttp import web
import json


def home(request):
    name = request.GET["name"]
    text = json.dumps("Hi {0}".format(name))
    return web.Response(body=text.encode("utf-8"), status=200, content_type="application/json")


def init_server(loop, host, port):
    app = web.Application()
    app.router.add_route('GET', "/", home)
    handler = app.make_handler()
    server = yield from loop.create_server(handler, host, port)
    return server.sockets[0].getsockname()


def main(host="127.0.0.1", port=2337):
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init_server(loop, host, port))
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:  # CTRL+C pressed
        pass
    print('Server shutting down.')
    loop.close()


if __name__ == "__main__":
    main()
