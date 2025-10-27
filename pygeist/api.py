from pygeist.abstract.api import AServer
from pygeist.abstract.idleness_handler import AIdlenessHandler
from pygeist.abstract.endpoint import AEndpoints


class APIMaster:
    def __init__(self,
                 server: AServer,
                 idleness_handler: AIdlenessHandler,
                 endpoints: AEndpoints,
                 ) -> None:
        self.server = server
        self.idleness_handler = idleness_handler
        self.endpoints = endpoints

    async def run(self):
        with self.idleness_handler as _idleness_handler:
            await self.server.run()
