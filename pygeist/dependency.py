from pygeist.abstract.dependency import Dependency


class Depends(Dependency):
    async def call_depend(self,
                          args: list = [],
                          kwargs: dict = {},
                          ):
        return await self.dependency(
            *args,
            **kwargs,
        )
