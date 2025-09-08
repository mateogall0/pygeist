from zeitgeist_server import idleness_handler
from zeitgeist_server.router import Endpoints
from zeitgeist_server.utils.singleton import singleton_class
from zeitgeist_server.registry import (Server,
                                       IdlenessHandler,
                                       APIMaster,)


@singleton_class
class ZeitgeistAPI:
    """
    Final API abstraction
    """
    def __init__(self,
                 port = 4000,
                 thread_pool_size = 4,
                 idleness_max_time = 60,
                 ) -> None:
        self.port = port
        self.thread_pool_size = thread_pool_size
        self.idleness_max_time = idleness_max_time

    def _compose(self) -> APIMaster:
        server = Server(self.port,
                        self.thread_pool_size)
        endpoints = Endpoints()
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
