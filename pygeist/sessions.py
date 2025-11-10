from typing import Any
from pygeist.adapter import _adapter


async def set_session_data(key: int, value: Any):
    return _adapter._set_session_meta(key, value)

async def get_session_data(key: int) -> Any:
    return _adapter._get_session_meta(key)

async def send_payload(key: int, payload: str):
    return _adapter._send_unrequested_payload(key, payload)
