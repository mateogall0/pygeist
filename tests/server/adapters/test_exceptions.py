from zeitgeist_server import _adapter
from zeitgeist_server.exceptions import (SessionsStructureInit,
                                         EndpointsInit,
                                         EndpointsDestruct,)
import pytest


def test_init_session_structure_reinit():
    _adapter._init_sessions_structure(
        idle_timeout=30,
        map_size=256
    )
    with pytest.raises(SessionsStructureInit):
        _adapter._init_sessions_structure(
            idle_timeout=30,
            map_size=256
        )
    _adapter._destroy_sessions_structure()

def test_init_session_structure_bad_size():
    with pytest.raises(SessionsStructureInit):
        _adapter._init_sessions_structure(
            idle_timeout=30,
            map_size=0
        )

def test_destroy_no_session_structure():
    with pytest.raises(EndpointsDestruct):
        _adapter._destroy_endpoints_list()

def test_init_endpoints_list_reinit():
    _adapter._init_endpoints_list()
    with pytest.raises(EndpointsInit):
        _adapter._init_endpoints_list()
    _adapter._destroy_endpoints_list()

def test_destroy_no_endpoints_list():
    with pytest.raises(EndpointsDestruct):
        _adapter._destroy_endpoints_list()
