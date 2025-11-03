import pytest
from pygeist.exceptions import ZEITException
from pygeist.request import Request
from pygeist.sessions import get_session_data, set_session_data
from . import zeit_app
import json
from pydantic import BaseModel

@pytest.fixture
def app(zeit_app):
    class User(BaseModel):
        name: str
        age: int

    async def get_u(req: Request):
        u = await get_session_data(req.client_key)
        if u is None:
            raise ZEITException(400)
        return u.model_dump()

    async def set_u(u: User, req: Request):
        await set_session_data(req.client_key, u)

    async def del_u(req: Request):
        await set_session_data(req.client_key, None)

    zeit_app.post('/', set_u, status_code=200)
    zeit_app.get('/', get_u, status_code=200)
    zeit_app.delete('/', del_u, status_code=204)

    yield zeit_app
