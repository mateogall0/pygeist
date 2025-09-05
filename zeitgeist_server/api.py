from zeitgeist_server.utils.singleton import singleton_class
from zeitgeist_server.abstract.api import AServer
from zeitgeist_server import _adapter
from zeitgeist_server.exceptions import ServerAlreadyStarted


@singleton_class(exc_cls=ServerAlreadyStarted)
class Server(AServer):
    def run(self,) -> None:
        pass
