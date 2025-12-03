import pytest
from pygeist.exceptions import ZEITException
from pygeist.request import Request
from pygeist.router import Router
from pygeist.sessions import get_session_data, set_session_data
from pygeist.unrequested_message import send_message
from pygeist.utils import status_code
from . import zeit_app
import json
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

waiting = []

async def get_u(req: Request):
    u = await get_session_data(req.client_key)
    if u is None:
        raise ZEITException(400)
    return u.model_dump()

async def set_u(u: User, req: Request):
    await set_session_data(req.client_key, u)

async def del_u(req: Request):
    await set_session_data(req.client_key, None)

async def broadcast(msg: str):
    for k in waiting:
        await send_message(k, msg)

async def wait_msg(req: Request):
    waiting.append(req.client_key)


@pytest.fixture
def app(zeit_app):

    zeit_app.post('/', set_u, status_code=200)
    zeit_app.get('/', get_u, status_code=200)
    zeit_app.delete('/', del_u, status_code=204)

    msgs_r = Router('/msgs')
    msgs_r.post('/', wait_msg, status_code=200)
    msgs_r.post('/broadcast', broadcast, status_code=200)

    zeit_app.include_router(msgs_r)


    yield zeit_app
