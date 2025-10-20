from pygeist import _adapter
import asyncio

async def set_session_data(key: int, value):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _adapter._set_session_meta, key, value)

async def get_session_data(key: int):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _adapter._get_session_meta, key)

async def send_payload(key: int, payload: str):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _adapter._send_unrequested_payload, key, payload)
