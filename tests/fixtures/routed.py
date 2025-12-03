from .socket import _find_free_port
import pytest
import multiprocessing
import socket
import time
from pygeist.zeitgeist import ZeitgeistAPI
from pygeist.router import Router
from pygeist.request import Request
from pygeist.sessions import send_payload

async def handler1515(req: Request):
    print('hi from 1515 handler')
    return 1515

async def handlerpow(req: Request):
    try:
        return int(req.body) ** 2
    except:
        return 'error'

async def handlerbye(req: Request):
    return 'bye'


async def handlerhello(req: Request):
    return 'hello'

def _build_example(port):
    r = Router('/')

    nested_r = Router('/hello')

    nested_r.get('/get-hello', handlerhello, status_code=200)

    nested_r2 = Router('/bye')

    nested_r2.get('/get-bye', handlerbye, status_code=200)

    nested_r.include_router(nested_r2)

    r.get('/get-1515', handler1515, status_code=200)
    r.get('/get-pow', handlerpow, status_code=200)
    api = ZeitgeistAPI(port=port)
    api.include_router(r)
    api.run()


@pytest.fixture
def example_routed_server() -> int:
    port = _find_free_port()
    server_process = multiprocessing.Process(target=_build_example,
                                             args=(port,))
    server_process.start()

    for _ in range(500):
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
