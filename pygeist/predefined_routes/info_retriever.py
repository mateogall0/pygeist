from pygeist.request import Request

_info: dict = {}

def set_info(info: dict):
    global _info
    _info = info

async def info_retriever_handler(req: Request) -> dict:
    return _info
