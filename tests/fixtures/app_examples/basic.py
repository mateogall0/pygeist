import pytest
from pygeist.request import Request
from . import zeit_app


@pytest.fixture
def app(zeit_app):
    async def main(req: Request):
        return 'Hello world!'

    async def main_str_json(req: Request):
        return '{"name": "Alice", "age": 30, "city": "London"}'

    zeit_app.get('/', main, status_code=200)
    zeit_app.get('/s', main, status_code=200)
    yield zeit_app
