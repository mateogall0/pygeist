from zeitgeist_server.zeitgeist import ZeitgeistAPI
from zeitgeist_server.router import Router
from zeitgeist_server.request import Request
import pytest
import time
import multiprocessing
import socket


def _build_example(port, ready_event):
    r = Router('/get-1515')
    async def handler(req: Request):
        return 1515

    r.get('/', handler)
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
