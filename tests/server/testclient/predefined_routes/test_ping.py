from pygeist.testclient import TestClient
from pygeist import ZeitgeistAPI
from tests.fixtures.socket import _find_free_port
import pytest


@pytest.mark.asyncio
async def test_async_requests():
    app = ZeitgeistAPI(_find_free_port())
    c = TestClient(app)
    await c.link()

    res = await c.get('/ping')
    assert res.status_code == 200
    body = res.body
    assert body == 'pong'

    await c.unlink()
