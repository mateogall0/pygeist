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
def test_request(app, target, status_code, expected):
    client = TestClient(app)
    print('before link')
    client.link()
    print('after link')
    res = client.get(target)
    print('after get')
    assert res.status_code == status_code
    assert res.body == expected, res
    client.unlink()
