from pygeist import _adapter
import asyncio

async def set_session_data(key: int, value):
    return await asyncio.create_task(_adapter._set_session_meta(key, value))

async def get_session_data(key: int):
    return await asyncio.create_task(_adapter._get_session_meta(key))

async def send_payload(key: int, payload: str):
    return await asyncio.create_task(_adapter._send_unrequested_payload(key, payload))
