from zeitgeist_server.utils.singleton import singleton_class
from zeitgeist_server.abstract.api import AServer
from zeitgeist_server import _adapter


@singleton_class
class Server(AServer):
    def run(self,) -> None:
        _run_server
