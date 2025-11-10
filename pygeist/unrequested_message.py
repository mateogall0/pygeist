from typing import Any
from .sessions import send_payload
from .adapter import _adapter
import json


class Message:
    def __init__(self,
                 client_key: int,
                 data: Any,
                 parsed_data: str,
                 ) -> None:
        self.client_key = client_key
        self.parsed_data = parsed_data
        self.data = data

async def send_message(client_key: int,
                       data: Any,
                       ) -> Message:
    parsed_data = data if isinstance(data, str) else json.dumps(data)
    msg = (
        f"{_adapter.MESSAGE_SIGNATURE}\r\n"
        f"Content-Length: {len(parsed_data)}\r\n\r\n"
        f"{parsed_data}"
    )
    await send_payload(client_key, msg)
    return Message(client_key, data, parsed_data)
