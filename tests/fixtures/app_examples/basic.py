import pytest
from pygeist.exceptions import ZEITException
from pygeist.request import Request
from . import zeit_app
import asyncio


@pytest.fixture
def app(zeit_app):
    async def main(req: Request):
        return 'Hello world!'

    async def main_str_json(req: Request):
        return '{"name": "Alice", "age": 30, "city": "London"}'

    async def main_with_exception(req: Request):
        raise ZEITException(401, 'cannot be accessed')

    async def main_with_unhandled(req: Request):
        raise TypeError('An errorr')

    async def slow_handler(req: Request):
        await asyncio.sleep(0.5)
        return "done"

    async def echo_handler(req: Request):
        await asyncio.sleep(0.5)
        return req.body

    async def echo_query_params(req: Request):
        return req.query_params

    zeit_app.get('/', main, status_code=200)
    zeit_app.post('/p', main, status_code=200)
    zeit_app.get('/s', main_str_json, status_code=200)
    zeit_app.get('/exception', main_with_exception, status_code=200)
    zeit_app.get('/unhandled', main_with_unhandled, status_code=200)
    zeit_app.get('/async', slow_handler, status_code=200)
    zeit_app.get('/async_echo', echo_handler, status_code=200)
    zeit_app.get('/echo_params', echo_query_params, status_code=200)
    yield zeit_app
