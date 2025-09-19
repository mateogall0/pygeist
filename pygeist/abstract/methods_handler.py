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
