from zeitgeist_server import _adapter
import pytest


@pytest.mark.parametrize("method",
                         [_adapter.POST,
                          _adapter.GET,
                          _adapter.DELETE,
                          _adapter.PUT])
def test_method_exists(method):
    assert isinstance(method, int)
