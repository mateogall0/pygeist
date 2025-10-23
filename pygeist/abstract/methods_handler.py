from abc import ABC, abstractmethod
from typing import Any

class AMethodsHandler(ABC):
    @abstractmethod
    def _method_handler(self,
                        method: str,
                        *ag,
                        **kw,
                        ) -> Any:
        pass

    def post(self,
             *ag,
             **kw):
        return self._method_handler('post', *ag, **kw)

    def get(self,
            *ag,
            **kw):
        return self._method_handler('get', *ag, **kw)

    def delete(self,
               *ag,
               **kw):
        return self._method_handler('delete', *ag, **kw)

    def put(self,
            *ag,
            **kw):
        return self._method_handler('put', *ag, **kw)



class AAsyncMethodsHandler(ABC):
    @abstractmethod
    async def _method_handler(self,
                              method: str,
                              *ag,
                              **kw,
                              ) -> Any:
        pass

    async def post(self,
                   *ag,
                   **kw):
        return await self._method_handler('post', *ag, **kw)

    async def get(self,
                  *ag,
                  **kw):
        return await self._method_handler('get', *ag, **kw)

    async def delete(self,
                     *ag,
                     **kw):
        return await self._method_handler('delete', *ag, **kw)

    async def put(self,
                  *ag,
                  **kw):
        return await self._method_handler('put', *ag, **kw)
