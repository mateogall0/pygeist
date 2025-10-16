from abc import ABC, abstractmethod


class AServer(ABC):
    def __init__(self,
                 port: int = 4000,
                 thread_pool_size: int = 4,
                 ) -> None:
        self.port: int = port
        self.thread_pool_size: int = thread_pool_size

    @abstractmethod
    async def run(self,
            ) -> None:
        pass
