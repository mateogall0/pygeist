import asyncio

_loop = None

def set_helper_loop(loop):
    global _loop
    _loop = loop


def run_handler(func, *ag, **kw):
    return func(*ag, **kw)
    # async def wrapper():
    #     return await asyncio.to_thread(func, *ag, **kw)

    # global _loop
    # if _loop is None:
    #     raise RuntimeError("Helper loop not set")

    # # thread-safe scheduling
    # _loop.call_soon_threadsafe(asyncio.create_task, wrapper())
