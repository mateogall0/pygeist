from pygeist.utils.singleton import singleton_class
from pygeist.abstract.api import AServer
from pygeist import _adapter
from pygeist.exceptions import ServerAlreadyStarted


@singleton_class(exc_cls=ServerAlreadyStarted)
class Server(AServer):
    def run(self,) -> None:
        try:
            _adapter._run_server(
                port=self.port,
                thread_pool_size=self.thread_pool_size,
            )
        except KeyboardInterrupt:
            pass
