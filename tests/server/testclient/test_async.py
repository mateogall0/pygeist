from pygeist.testclient import TestClient
from tests.fixtures.app_examples.basic import app, zeit_app
import pytest
import asyncio
import time


@pytest.mark.asyncio
async def test_async_requests(app):
    client0 = TestClient(app)
    client1 = TestClient(app,
                         create_server=False)
    client2 = TestClient(app,
                         create_server=False)
    await client0.link()
    await client1.link()
    await client2.link()

    start = time.time()
    results = await asyncio.gather(client0.get('/async'),
                                   client1.get('/async'),
                                   client2.get('/async'),)
    end = time.time()

    for r in results:
        assert r.status_code == 200
        assert r.body == 'done'

    final_time = end - start
    assert final_time < 1
    await client0.unlink()
    await client1.unlink()
    await client2.unlink()

@pytest.mark.asyncio
async def test_async_echo_requests(app):
    client0 = TestClient(app)
    client1 = TestClient(app, create_server=False)
    client2 = TestClient(app, create_server=False)

    await client0.link()
    await client1.link()
    await client2.link()

    payloads = [
        "hello0",
        "hello1",
        "hello2",
    ]

    start = time.time()
    results = await asyncio.gather(
        client0.get("/async_echo", data=payloads[0]),
        client1.get("/async_echo", data=payloads[1]),
        client2.get("/async_echo", data=payloads[2]),
    )
    end = time.time()

    for i, r in enumerate(results):
        assert r.status_code == 200
        assert r.body == payloads[i], f"Client {i} got mismatched echo"

    bodies = [r.body for r in results]
    assert len(bodies) == len(set(map(str, bodies))), "Echo responses not unique"

    final_time = end - start
    assert final_time < 1

    await client0.unlink()
    await client1.unlink()
    await client2.unlink()
