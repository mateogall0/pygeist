import inspect
from typing import Callable


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
