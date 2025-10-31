from tests.fixtures.app_examples.modeled import zeit_app, app
import pytest
from pygeist import TestClient


@pytest.mark.asyncio
@pytest.mark.parametrize("age, status, expected", [
    (21, 200, True),
    (18, 200, True),
    (10, 200, False),
    (17, 200, False),
    ('invalid', 422, None),
    ('21', 200, True),
])
async def test_user_res(app, age, status, expected):
    c = TestClient(app)
    await c.link()

    res = await c.get('/isadult', data={'name': 'test', 'age': age})

    assert res.status_code == status

    if expected is not None:
        assert res.body == expected

    await c.unlink()

@pytest.mark.asyncio
@pytest.mark.parametrize("value, status", [
    (50.5, 200),
    (50, 200),
    (0.0, 200),
    (0.1, 200),
    (0, 200),
    ('55.5', 200),
    ('invalid', 422),
    (None, 422),
])
async def test_echo_float_param(app, value, status):
    c = TestClient(app)
    await c.link()

    if value is None:
        res = await c.get(f'/echo_float')
    else:
        res = await c.get(f'/echo_float?value={value}')

    assert res.status_code == status
    if status == 200:
        assert res.body == float(value)

    await c.unlink()

@pytest.mark.asyncio
@pytest.mark.parametrize("value, age, status, expected", [
    (21, 18, 200, True),
    (17, 18, 200, False),
])
async def test_combined_param_body(app, value, age, status, expected):
    c = TestClient(app)
    await c.link()

    res = await c.get(f'/is_age_greater?age={value}', data={'name': 'test', 'age': age})
    assert res.status_code == status

    assert res.body == expected

    await c.unlink()

@pytest.mark.asyncio
@pytest.mark.parametrize("values", [
    [12.5, 50.5, 0.5],
    [0, 0, 0, 0, 0],
    [5, 1, 1024, 5555555555, 1231231, 123 ,123 ,123],
])
async def test_echo_float_list_param(app, values):
    c = TestClient(app)
    await c.link()

    url = f'/echo_float_list?{"&".join(f"values={v}" for v in values)}'
    res = await c.get(url)

    assert res.status_code == 200
    assert sorted(res.body) == sorted(values)

    await c.unlink()
