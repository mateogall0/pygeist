from zeitgeist_server.zeitgeist import ZeitgeistAPI
from zeitgeist_server.router import Router
from zeitgeist_server.request import Request
from zeitgeist_server.sessions import send_payload
import pytest
import multiprocessing
import socket


def _build_example(port, ready_event):
    last_requested_id = None
    r = Router('/')
    async def handler1515(req: Request):
        return 1515

    async def handlerpow(req: Request):
        try:
            return int(req.body) ** 2
        except:
            return 'error'

    async def broadcast(req: Request):
        nonlocal last_requested_id
        if last_requested_id is not None:
            send_payload(last_requested_id, req.body)
        last_requested_id = req.client_key
        return 'sending stuff'

    r.get('/get-1515', handler1515)
    r.get('/get-pow', handlerpow)
    r.post('/post-broadcast', broadcast)
    api = ZeitgeistAPI(port=port)
    ready_event.set()
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
    ready_event = multiprocessing.Event()
    server_process = multiprocessing.Process(target=_build_example,
                                             args=(port,ready_event))
    server_process.start()
    ready_event.wait(timeout=5)
    try:
        yield port
    finally:
        server_process.terminate()
        server_process.join()
