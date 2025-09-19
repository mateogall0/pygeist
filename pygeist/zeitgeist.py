from pygeist.router import Endpoints, Router
from pygeist.utils.singleton import singleton_class
from pygeist.registry import (Server,
                              IdlenessHandler,
                              APIMaster,)


class _APIRouter:
    def __init__(self,
                 main_prefix='',
                 ) -> None:
        self.router = Router(main_prefix)

    def include_router(self, router: Router) -> None:
        self.router.include_router(router)

    def init_endpoints(self):
        self.router.create_endpoints_from_buf()

    def post(self,
             *ag,
             **kw) -> None:
        self.router.post(*ag, **kw)

    def get(self,
            *ag,
            **kw) -> None:
        self.router.get(*ag, **kw)

    def delete(self,
               *ag,
               **kw) -> None:
        self.router.delete(*ag, **kw)

    def put(self,
            *ag,
            **kw) -> None:
        self.router.put(*ag, **kw)


@singleton_class
class ZeitgeistAPI(_APIRouter):
    """
    Final API abstraction
    """
    def __init__(self,
                 port = 4000,
                 main_prefix='',
                 thread_pool_size = 4,
                 idleness_max_time = 60,
                 ) -> None:
        self.port = port
        self.thread_pool_size = thread_pool_size
        self.idleness_max_time = idleness_max_time
        super().__init__(main_prefix)

    def _compose(self) -> APIMaster:
        server = Server(self.port,
                        self.thread_pool_size)
        endpoints = Endpoints()
        self.init_endpoints()
        idleness_handler = IdlenessHandler(self.idleness_max_time)
        return APIMaster(
            server,
            idleness_handler,
            endpoints,
        )

    def _run(self,
             api_master: APIMaster,
             ) -> None:
        api_master.run()

    def run(self) -> None:
        api_master = self._compose()
        print(f'Starting server on port {self.port}...')
        print('press Ctrl+C to stop it')
        self._run(api_master)
        print('\nstopped')
