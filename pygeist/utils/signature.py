import inspect
from typing import Callable, Any
from pygeist.request import Request
from pydantic import BaseModel


def process_signature(handler: Callable,
                      ) -> tuple[dict[str, type], type | None]:
    sig = inspect.signature(handler)
    params = {}

    for name, param in sig.parameters.items():
        annotation = param.annotation
        if annotation is inspect._empty:
            annotation = None
        params[name] = annotation

    return_annotation = sig.return_annotation
    if return_annotation is inspect._empty:
        return_annotation = None

    return params, return_annotation


async def params_filter(params: dict[str, type],
                        req: Request,
                        ) -> dict[str, Any]:
    kw = {}
    for k, v in params.items():
        if v == Request:
            kw[k] = req
        elif issubclass(v, BaseModel):
            kw[k] = v(**req.body)
        elif v == dict:
            kw[k] = req.body
    return kw
