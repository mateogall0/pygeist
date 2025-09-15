import asyncio, threading

_loop = None
_thread = None

def _start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def get_loop():
    global _loop, _thread
    if _loop is None:
        _loop = asyncio.new_event_loop()
        _thread = threading.Thread(target=_start_loop, args=(_loop,), daemon=True)
        _thread.start()
    return _loop
