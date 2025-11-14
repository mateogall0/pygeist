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
@pytest.mark.parametrize("num_clients,messages", [
    (2, ["hello", "world"]),
    (3, ["foo", "bar", "baz"]),
    (5, ["ping"]),
])
async def test_broadcast(fixture_app, num_clients, messages):
    broadcaster = TestClient(fixture_app)
    await broadcaster.link()

    listeners = [TestClient(fixture_app, create_server=False) for _ in range(num_clients)]
    for c in listeners:
        await c.link()
        res = await c.post('/msgs/')
        assert res.status_code == 200

    for msg_text in messages:
        res = await broadcaster.post(f'/msgs/broadcast?msg={msg_text}')
        assert res.status_code == 200

        for c in listeners:
            msg = await c.receive()
            assert msg.body == msg_text

    for c in listeners:
        await c.unlink()
    await broadcaster.unlink()
