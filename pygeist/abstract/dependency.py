from abc import ABC, abstractmethod
from typing import Callable


class Dependency(ABC):
    @abstractmethod
    async def call_depend(self,
                          args: list = [],
                          kwargs: dict = {},
                          ):
        pass
