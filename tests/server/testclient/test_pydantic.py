from tests.fixtures.app_examples.modeled import zeit_app, app
import pytest
from pygeist import TestClient


@pytest.mark.asyncio
@pytest.mark.parametrize("age, expected", [
    (21, True),
    (18, True),
    (10, False),
    (17, False),
])
async def test_user_res(app, age, expected):
    c = TestClient(app)
    await c.link()

    res = await c.get('/isadult', data={'name': 'test', 'age': age})

    assert res.status_code == 200

    assert res.body == expected

    await c.unlink()
