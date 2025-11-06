from pygeist.zeitgeist import ZeitgeistAPI
from tests.fixtures.app_examples.sessioned import zeit_app, app as fixture_app
import pytest
import asyncio
from pygeist import TestClient


@pytest.mark.asyncio
async def test_set_get_user(fixture_app):
    c = TestClient(fixture_app)
    await c.link()

    res = await c.get('/')
    assert res.status_code == 400

    res = await c.post('/', data={'name': 'test', 'age': 21})
    assert res.status_code == 200

    res = await c.get('/')
    assert res.status_code == 200
    assert res.body == {'name': 'test', 'age': 21}

    res = await c.delete('/')
    assert res.status_code == 204

    res = await c.get('/')
    assert res.status_code == 400

    await c.unlink()

@pytest.mark.asyncio
async def test_session_timeout():
    app = ZeitgeistAPI(idleness_max_time=1)

    async def main():
        return 'ok'

    app.get('/', main, status_code=200)

    c = TestClient(app)
    await c.link()
    res = await c.get('/')
    assert res.status_code == 200
    await asyncio.sleep(2)
    with pytest.raises(ConnectionError):
        res = await c.get('/')
