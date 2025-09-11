from zeitgeist_server import _adapter


def set_session_data(key: int, value):
    return _adapter._set_session_meta(key, value)

def get_session_data(key: int):
    return _adapter._get_session_meta(key)

def send_payload(key: int, payload: str) -> None:
    return _adapter._send_unrequested_payload(key, payload)
