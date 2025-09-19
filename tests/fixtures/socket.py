from pygeist.zeitgeist import ZeitgeistAPI
from pygeist.router import RouterRigistry
from pygeist.request import Request
from pygeist.sessions import send_payload
import pytest
import multiprocessing
import socket
import time


def _build_example(port):
    last_requested_id = None
    r = RouterRigistry('/')
    async def handler1515(req: Request):
        await send_payload(req.client_key, str(1515))

    async def handlerpow(req: Request):
        try:
            await send_payload(req.client_key, str(int(req.body) ** 2))
        except:
            await send_payload(req.client_key, 'error')

    async def broadcast(req: Request):
        nonlocal last_requested_id
        if last_requested_id is not None:
            await send_payload(last_requested_id, req.body)
        last_requested_id = req.client_key
        await send_payload(req.client_key, 'sending stuff')

    r.get('/get-1515', handler1515)
    r.get('/get-pow', handlerpow)
    r.post('/post-broadcast', broadcast)
    api = ZeitgeistAPI(port=port)
    api.run()

def _find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture
def example_server() -> int:
    port = _find_free_port()
    server_process = multiprocessing.Process(target=_build_example,
                                             args=(port,))
    server_process.start()

    for _ in range(50):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                break
        except OSError:
            time.sleep(0.001)
    else:
        raise RuntimeError("server did not start in time")

    try:
        yield port
    finally:
        server_process.terminate()
        server_process.join()
