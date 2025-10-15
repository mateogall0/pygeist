from pygeist.testclient import TestClient
from tests.fixtures.app_examples.basic import app, zeit_app
import pytest


@pytest.mark.parametrize("target,expected", [
    ('/', 'Hello world!'),
])
def test_request(app, target, expected):
    client = TestClient(app)
    client.link()
    res = client.get(target)
    assert res.body == expected, res
    client.unlink()
