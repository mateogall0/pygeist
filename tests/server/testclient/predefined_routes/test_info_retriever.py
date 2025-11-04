from pygeist.testclient import TestClient
from pygeist import ZeitgeistAPI
from tests.fixtures.socket import _find_free_port
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("idleness_max_time", [
    64,
    1024,
    8192,
])
async def test_async_requests(idleness_max_time):
    app = ZeitgeistAPI(_find_free_port(), idleness_max_time=idleness_max_time)
    c = TestClient(app)
    await c.link()

    res = await c.get('/meta')
    assert res.status_code == 200
    body = res.body
    assert body['idleness_max_time'] == idleness_max_time

    await c.unlink()
