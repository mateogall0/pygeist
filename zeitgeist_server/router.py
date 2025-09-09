from zeitgeist_server import _adapter
from typing import Callable
from zeitgeist_server.abstract.endpoint import AEndpoints
from zeitgeist_server.exceptions import EndpointsDestruct


class Endpoints(AEndpoints):
    def __del__(self) -> None:
        try:
            _adapter._destroy_endpoints_list()
        except EndpointsDestruct:
            pass

    def print_all(self) -> None:
        _adapter._pall_endpoints()


class Router:
    def __init__(self,
                 prefix='',
                 tags=[],
                 ) -> None:
        self.tags = tags
        self.prefix = prefix

    def create_endpoint(self,
                        method: int,
                        target: str,
                        handler: Callable,
                        *ag,
                        **kw,
                        ) -> None:
        final_target = self.prefix
        if final_target[-1] == '/':
            final_target = final_target[:-1]
        final_target +=  target
        _adapter._create_endpoint(
            method=method,
            target=final_target,
            handler=handler,
            *ag,
            **kw
        )

    def post(self,
             *ag,
             **kw) -> None:
        self.create_endpoint(_adapter.POST,
                             *ag,
                             **kw)

    def get(self,
            *ag,
            **kw) -> None:
        self.create_endpoint(_adapter.GET,
                             *ag,
                             **kw)
    def delete(self,
               *ag,
               **kw) -> None:
        self.create_endpoint(_adapter.DELETE,
                             *ag,
                             **kw)

    def put(self,
            *ag,
            **kw) -> None:
        self.create_endpoint(_adapter.PUT,
                             *ag,
                             **kw)
