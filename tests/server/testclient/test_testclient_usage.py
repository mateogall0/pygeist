from pygeist.testclient import TestClient
from tests.fixtures.app_examples.basic import app, zeit_app
import pytest


@pytest.mark.parametrize("target,status_code,expected", [
    ('/', 200, 'Hello world!'),
    ('/p', 405, '405 Method not allowed'),
    ('/s', 200, {"name": "Alice", "age": 30, "city": "London"}),
    ('/exception', 401, 'cannot be accessed'),
    ('/nonexistent_route', 404, '404 Resource not found'),
    ('/unhandled', 500, '500 Internal server error')
])
@pytest.mark.asyncio
async def test_enter_exit(app, target, status_code, expected):
    _client = TestClient(app)
    assert _client.reader is None
    assert _client.writer is None

    async with _client as client:
        assert _client.reader is not None
        assert _client.writer is not None

        res = await client.get(target)
        assert res.status_code == status_code
        assert res.body == expected, res

    assert _client.reader is None
    assert _client.writer is None
