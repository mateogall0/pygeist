from zeitgeist_server.utils.singleton import singleton_class
from zeitgeist_server.abstract.api import AServer
from zeitgeist_server.abstract.idleness_handler import AIdlenessHandler


@singleton_class
class _APIMaster:
    def __init__(self,
                 server: AServer,
                 idleness_handler: AIdlenessHandler,
                 ) -> None:
        self.server = server
        self.idleness_handler = idleness_handler

    def run(self):
        with self.idleness_handler as _idleness_handler:
            self.server.run()
