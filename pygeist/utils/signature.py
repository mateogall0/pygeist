import inspect
from typing import Callable, Any, Dict, List, get_origin, get_args
from pygeist.abstract.request import ARequest
from pydantic import BaseModel, TypeAdapter
from pygeist.abstract.dependency import Dependency

def safe_issubclass(obj, parent):
    return isinstance(obj, type) and issubclass(obj, parent)


def process_signature(handler: Callable,
                      ) -> tuple[dict[str, tuple[type, Any]],
                                 type | None]:
    sig = inspect.signature(handler)
    params = {}

    for name, param in sig.parameters.items():
        annotation = param.annotation
        if annotation is inspect._empty:
            annotation = None
        default_val = param.default
        if default_val is inspect._empty:
            default_val = None
        params[name] = (annotation,
                        default_val)

    return_annotation = sig.return_annotation
    if return_annotation is inspect._empty:
        return_annotation = None

    return params, return_annotation

async def params_filter(params: dict[str, tuple[type, Any]],
                        req: ARequest,
                        ) -> dict[str, Any]:
    kw = {}

    for k, whole_sig in params.items():
        v, default_val = whole_sig
        if isinstance(default_val, Dependency):
            kw[k] = await default_val.call_depend([req])
        elif safe_issubclass(v, ARequest):
            kw[k] = req

        elif safe_issubclass(v, BaseModel):
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
