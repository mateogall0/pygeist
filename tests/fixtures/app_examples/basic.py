import pytest
from pygeist.request import Request
from . import zeit_app


@pytest.fixture
def app(zeit_app):
    async def main(req: Request):
        return 'Hello world!'
    zeit_app.get('/', main)
    yield zeit_app
