from pygeist.router import Endpoints, Router
from pygeist.registry import (Server,
                              IdlenessHandler,
                              APIMaster,)
from pygeist.abstract.methods_handler import AMethodsHandler
from pygeist.concurrency.helpers import worker, set_helper_loop
import asyncio
from .predefined_routes import info_retriever


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
                 workers = 4,
                 ) -> None:
        self.port = port
        self.idleness_max_time = idleness_max_time
        self.workers = workers
        super().__init__(main_prefix)

    def _compose(self) -> APIMaster:
        info_retriever.set_info({
            'idleness_max_time': self.idleness_max_time,
        })
        self.get('/meta',
                 info_retriever.info_retriever_handler,
                 status_code=200,)

        server = Server(self.port)
        endpoints = Endpoints()
        self.init_endpoints()
        idleness_handler = IdlenessHandler(self.idleness_max_time)
        return APIMaster(
            server,
            idleness_handler,
            endpoints,
        )

    async def _run(self,
                   api_master: APIMaster,
                   ) -> None:

        set_helper_loop(asyncio.get_event_loop())
        worker_tasks = [worker() for _ in range(self.workers)]

        await asyncio.gather(
            *worker_tasks,
            api_master.run(),
        )

    def run(self) -> None:
        api_master = self._compose()
        print(f'Starting server on port {self.port}...')
        print('press Ctrl+C to stop it')
        asyncio.run(self._run(api_master))
        print('\nstopped')
