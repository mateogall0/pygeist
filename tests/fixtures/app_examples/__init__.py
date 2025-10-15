import pytest
from pygeist.zeitgeist import ZeitgeistAPI
from ..socket import _find_free_port

@pytest.fixture
def zeit_app() -> ZeitgeistAPI:
    ZeitgeistAPI._reset_instance()
    yield ZeitgeistAPI(port=_find_free_port())
