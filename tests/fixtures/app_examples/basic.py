import pytest
from pygeist.exceptions import ZEITException
from pygeist.request import Request
from . import zeit_app


@pytest.fixture
def app(zeit_app):
    async def main(req: Request):
        return 'Hello world!'

    async def main_str_json(req: Request):
        return '{"name": "Alice", "age": 30, "city": "London"}'

    async def main_with_exception(req: Request):
        raise ZEITException(401, 'cannot be accessed')

    zeit_app.get('/', main, status_code=200)
    zeit_app.get('/s', main_str_json, status_code=200)
    zeit_app.get('/exception', main_with_exception, status_code=200)
    yield zeit_app
