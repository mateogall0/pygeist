from pygeist.utils.singleton import singleton_class
from pygeist.abstract.api import AServer
from pygeist import _adapter
from pygeist.exceptions import ServerAlreadyStarted
import asyncio


class Server(AServer):
    async def run(self,) -> None:
        try:
            await asyncio.to_thread(
                _adapter._run_server,
                self.port,
            )
        except KeyboardInterrupt:
            pass
