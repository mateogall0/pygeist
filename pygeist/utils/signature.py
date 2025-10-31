import inspect
from typing import Callable, Any, Dict, List, get_origin, get_args
from pygeist.request import Request
from pydantic import BaseModel, TypeAdapter


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

        elif isinstance(v, type) and issubclass(v, BaseModel):
            kw[k] = v(**req.body)

        elif v in (dict, Dict):
            if not isinstance(req.body, dict):
                raise ValueError(f"Expected dict for {k}")
            kw[k] = req.body

        else:
            if k not in req.query_params:
                raise ValueError(f"Missing query parameter: {k}")
            values = req.query_params[k]

            origin = get_origin(v)
            args = get_args(v)

            if origin in (list, List):
                inner_type = args[0] if args else str
                adapter = TypeAdapter(list[inner_type])
                kw[k] = adapter.validate_python(values)

            else:
                adapter = TypeAdapter(v)
                kw[k] = adapter.validate_python(values[0])

    return kw
