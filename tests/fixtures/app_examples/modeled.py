import pytest
from pygeist.exceptions import ZEITException
from pygeist.request import Request
from . import zeit_app
import asyncio
from pydantic import BaseModel

@pytest.fixture
def app(zeit_app):
    class UserModel(BaseModel):
        name: str
        age: int

    async def main(req: Request):
        return {'name': 'test', 'age': 21}

    zeit_app.get('/', main, status_code=200, response_model=UserModel)
    yield zeit_app
