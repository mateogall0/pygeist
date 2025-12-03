from pygeist.adapter import _adapter
from typing import Callable, Any
from pygeist.abstract.endpoint import AEndpoints
from pygeist.exceptions import EndpointsDestruct, ZEITException
from pygeist.request import Request
from .sessions import send_payload
from pygeist.abstract.methods_handler import AMethodsHandler
import json
import traceback
from pygeist.utils import signature as sig_util


class WrappedEndpoint:
    def __init__(self,
                 handler: Callable,
                 params_info: Any,
                 response_model: Any | None,
                 status_code: int):
        self.handler =  handler
        self.params_info = params_info
        self.response_model = response_model
        self.status_code = status_code

    async def __call__(self, req: Request):
        handler = self.handler

        params = self.params_info
        try:
            kw = await sig_util.params_filter(params, req)
        except (ValueError, TypeError, KeyError, IndexError):
            zex = ZEITException(422, '422 Unprocessable entity')
            fres = zex.get_fres(_adapter.SERVER_VERSION, req)
            await send_payload(req.client_key, fres)
            _adapter._log_request(req.method, req.target, 422)
            return

        try:
            result = await self.handler(**kw)
            body = result if isinstance(result, str) else json.dumps(result)
            fres = (
                f"{_adapter.SERVER_VERSION} {self.status_code} {req.rid}\r\n"
                f"Content-Length: {len(body)}\r\n\r\n"
                f"{body}"
            )
            await send_payload(req.client_key, fres)
            _adapter._log_request(req.method, req.target, self.status_code)
        except ZEITException as zex:
            fres = zex.get_fres(_adapter.SERVER_VERSION, req)
            await send_payload(req.client_key, fres)
            _adapter._log_request(req.method, req.target, zex._status_code)
        except Exception:
            traceback.print_exc()
            zex = ZEITException(500, '500 Internal server error')
            fres = zex.get_fres(_adapter.SERVER_VERSION, req)
            await send_payload(req.client_key, fres)
            _adapter._log_request(req.method, req.target, 500)


class Endpoints(AEndpoints):
    def __del__(self) -> None:
        try:
            _adapter._destroy_endpoints_list()
        except EndpointsDestruct:
            pass

    def print_all(self) -> None:
        _adapter._pall_endpoints()


class RouterRigistry(AMethodsHandler):
    def __init__(self,
                 prefix='',
                 tags=[],
                 ) -> None:
        self.tags = tags
        self.prefix = prefix

    def _join_paths(self, target: str) -> str:
        prefix = self.prefix
        if not prefix.endswith("/"):
            prefix += "/"
        if target.startswith("/"):
            target = target[1:]
        return prefix + target

    def create_endpoint(self,
                        method: int,
                        target: str,
                        handler: Callable,
                        *ag,
                        **kw,
                        ) -> None:
        final_target = self._join_paths(target)
        _adapter._create_endpoint(
            method=method,
            target=final_target,
            handler=handler,
            *ag,
            **kw
        )

    def _method_handler(self, method: str, *ag, **kw):
        method_const = getattr(_adapter, method.upper())
        self.create_endpoint(method_const,
                             *ag,
                             **kw)

class Router(RouterRigistry):
    def __init__(self,
                 prefix='',
                 tags=[]) -> None:
        self._buff: list = []
        self._included: list[Router] = []
        super().__init__(prefix, tags)

    def include_router(self, router) -> None:
        router.prefix = self._join_paths(router.prefix)
        self._included.append(router)

    def create_endpoint(self,
                        method: int,
                        target: str,
                        handler: Callable,
                        status_code: int,
                        response_model: type | None = None,
                        *ag,
                        **kw,
                        ) -> None:
        params, _ = sig_util.process_signature(handler)

        wrapped_handler = WrappedEndpoint(
            handler,
            params,
            response_model,
            status_code,
        )

        self._buff.append((method, target, wrapped_handler, ag, kw))

    def create_endpoints_from_buf(self) -> None:
        for method, target, handler, ag, kw in self._buff:
            super().create_endpoint(method, target, handler, *ag, **kw)
        self._buff.clear()
        for i in self._included:
            i.create_endpoints_from_buf()
