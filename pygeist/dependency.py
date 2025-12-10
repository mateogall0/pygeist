from pygeist.abstract.dependency import Dependency
from typing import Callable


class Depends(Dependency):
    def __init__(self,
             dependency: Callable,
             ) -> None:
        self.dependency = dependency

    async def call_depend(self,
                          args: list = [],
                          kwargs: dict = {},
                          ):
        return await self.dependency(
            *args,
            **kwargs,
        )
