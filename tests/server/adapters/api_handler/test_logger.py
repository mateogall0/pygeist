from zeitgeist_server import _adapter


def test_get_logger_value():
    assert isinstance(_adapter._get_api_log(), bool)

def test_set_logger_value():
    _adapter._set_api_log(True)
    assert _adapter._get_api_log() == True
    _adapter._set_api_log(False)
    assert _adapter._get_api_log() == False
    _adapter._set_api_log(True)
    assert _adapter._get_api_log() == True
