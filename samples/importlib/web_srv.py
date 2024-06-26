"""Example for aiohttp.web basic server."""

import textwrap

from aiohttp import web


async def intro(request: web.Request) -> web.StreamResponse:
    txt = textwrap.dedent(
        """\
        Type {url}/hello/John  {url}/simple or {url}/change_body
        in browser url bar
    """
    ).format(url="127.0.0.1:8080")
    binary = txt.encode("utf8")
    resp = web.StreamResponse()
    resp.content_length = len(binary)
    resp.content_type = "text/plain"
    await resp.prepare(request)
    await resp.write(binary)
    return resp


async def simple(request: web.Request) -> web.StreamResponse:  # noqa: ARG001
    return web.Response(text="Simple answer")


async def change_body(
    request: web.Request,  # noqa: ARG001
) -> web.StreamResponse:
    resp = web.Response()
    resp.body = b"Body changed"
    resp.content_type = "text/plain"
    return resp


async def hello(request: web.Request) -> web.StreamResponse:
    resp = web.StreamResponse()
    name = request.match_info.get("name", "Anonymous")
    answer = ("Hello, " + name).encode("utf8")
    resp.content_length = len(answer)
    resp.content_type = "text/plain"
    await resp.prepare(request)
    await resp.write(answer)
    await resp.write_eof()
    return resp


def init() -> web.Application:
    app = web.Application()
    app.router.add_get("/", intro)
    app.router.add_get("/simple", simple)
    app.router.add_get("/change_body", change_body)
    app.router.add_get("/hello/{name}", hello)
    app.router.add_get("/hello", hello)
    return app


web.run_app(init())
