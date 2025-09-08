from zeitgeist_server.utils.singleton import singleton_class
from zeitgeist_server.abstract.api import AServer
from zeitgeist_server import _adapter
from zeitgeist_server.exceptions import ServerAlreadyStarted


@singleton_class(exc_cls=ServerAlreadyStarted)
class Server(AServer):
    def run(self,) -> None:
        try:
            print(f'Starting server on port {self.port}...')
            print('press Ctrl+C to stop it')
            _adapter._run_server(
                port=self.port,
                thread_pool_size=self.thread_pool_size,
            )
        except KeyboardInterrupt:
            print('\nstopped')
