from pygeist.router import Endpoints, Router
from pygeist.utils.singleton import singleton_class
from pygeist.registry import (Server,
                              IdlenessHandler,
                              APIMaster,)
from pygeist.abstract.methods_handler import AMethodsHandler
from pygeist.concurrency.helpers import set_helper_loop
import asyncio


class _APIRouter(AMethodsHandler):
    def __init__(self,
                 main_prefix='',
                 ) -> None:
        self.router = Router(main_prefix)

    def include_router(self, router: Router) -> None:
        self.router.include_router(router)

    def init_endpoints(self):
        self.router.create_endpoints_from_buf()

    def _method_handler(self, method: str, *ag, **kw):
        handler = getattr(self.router, method)
        handler(*ag, **kw)

class ZeitgeistAPI(_APIRouter):
    """
    Final API abstraction
    """
    def __init__(self,
                 port = 4000,
                 main_prefix='',
                 idleness_max_time = 60,
                 ) -> None:
        self.port = port
        self.idleness_max_time = idleness_max_time
        super().__init__(main_prefix)

    def _compose(self) -> APIMaster:
        server = Server(self.port)
        endpoints = Endpoints()
        self.init_endpoints()
        idleness_handler = IdlenessHandler(self.idleness_max_time)
        return APIMaster(
            server,
            idleness_handler,
            endpoints,
        )

    def _run(self, api_master: APIMaster) -> None:
        loop = asyncio.new_event_loop()
        set_helper_loop(loop)
        asyncio.set_event_loop(loop)
        loop.create_task(api_master.run())
        loop.run_forever()

    def run(self) -> None:
        api_master = self._compose()
        print(f'Starting server on port {self.port}...')
        print('press Ctrl+C to stop it')
        self._run(api_master)
        print('\nstopped')
