from tests.fixtures.app_examples.sessioned import zeit_app, app
import pytest
from pygeist import TestClient


@pytest.mark.asyncio
async def test_set_get_user(app):
    c = TestClient(app)
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
