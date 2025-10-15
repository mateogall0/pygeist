from pygeist.testclient import TestClient
from tests.fixtures.app_examples.basic import app, zeit_app
import pytest


@pytest.mark.parametrize("target,status_code,expected", [
    ('/', 200, 'Hello world!'),
    ('/s', 200, {"name": "Alice", "age": 30, "city": "London"}),
    ('/exception', 401, 'cannot be accessed'),
])
def test_request(app, target, status_code, expected):
    client = TestClient(app)
    client.link()
    res = client.get(target)
    assert res.status_code == status_code
    assert res.body == expected, res
    client.unlink()
