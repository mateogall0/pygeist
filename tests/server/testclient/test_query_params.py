from tests.fixtures.app_examples.basic import zeit_app, app
import pytest
from pygeist import TestClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            "hello=world0&goodbye=world1",
            {"hello": ["world0"], "goodbye": ["world1"]},
        ),
        (
            "a=1&a=2&a=3",
            {"a": ["1", "2", "3"]},
        ),
        (
            "x=42",
            {"x": ["42"]},
        ),
        (
            "param_with_space=hello%20world",
            {"param_with_space": ["hello world"]},
        ),
        (
            "empty=",
            {},
        ),
        (
            "repeated=one&repeated=two&other=three",
            {"repeated": ["one", "two"], "other": ["three"]},
        ),
        (
            "",
            {},
        ),
    ],
)
async def test_echo_params(app, query, expected):
    c = TestClient(app)
    await c.link()

    res = await c.get(f"/echo_params?{query}")
    assert res.status_code == 200
    assert res.body == expected

    await c.unlink()
