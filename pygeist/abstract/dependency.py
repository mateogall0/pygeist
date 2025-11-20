from abc import ABC, abstractmethod
from typing import Callable


class Dependency(ABC):
    def __init__(self,
                 dependency: Callable,
                 ) -> None:
        self.dependency = dependency

    @abstractmethod
    async def call_depend(self,
                          args: list = [],
                          kwargs: dict = {},
                          ):
        pass
