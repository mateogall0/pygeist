from tests.fixtures.app_examples.modeled import zeit_app, app
import pytest
from pygeist import TestClient


@pytest.mark.asyncio
@pytest.mark.parametrize("data, expected", [
    (None, False),
    ({'update': 0.0}, False),
    ({'update': None}, False),
    ({'update': 'wrong'}, False),
    ({'update':-500}, False),
    ({'update':-500.5}, False),
    ({'update':1}, True),
    ({'update':1.1}, True),
])

async def test_echo_float_param(app, data, expected):
    c = TestClient(app)
    await c.link()

    res = await c.get('/with_depend', data=data)
    assert res.status_code == 200
    assert res.body == expected

    await c.unlink()
