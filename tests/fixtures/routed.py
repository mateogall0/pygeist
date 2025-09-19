from .socket import _find_free_port
import pytest
import multiprocessing
from pygeist.zeitgeist import ZeitgeistAPI
from pygeist.router import Router
from pygeist.request import Request
from pygeist.sessions import send_payload


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
            await send_payload(last_requested_id, req.body)
        last_requested_id = req.client_key
        return 'sending stuff'

    nested_r = Router('/hello')

    async def handlerhello(req: Request):
        return 'hello'

    nested_r.get('/get-hello', handlerhello)

    nested_r2 = Router('/bye')

    async def handlerbye(req: Request):
        return 'bye'

    nested_r2.get('/get-bye', handlerbye)

    nested_r.include_router(nested_r2)

    r.include_router(nested_r)

    r.get('/get-1515', handler1515)
    r.get('/get-pow', handlerpow)
    r.post('/post-broadcast', broadcast)
    api = ZeitgeistAPI(port=port)
    api.include_router(r)
    ready_event.set()
    api.run()


@pytest.fixture
def example_routed_server() -> int:
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
