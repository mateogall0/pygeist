from pygeist.testclient import TestClient
from tests.fixtures.app_examples.basic import app, zeit_app


def test_request(app):
    client = TestClient(app)
    client.connect()
    res = client.get('/')
    assert res.payload == 'Hello world!'
    client.disconnect()
