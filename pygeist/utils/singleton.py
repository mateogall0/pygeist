from functools import wraps
from threading import Lock
import weakref

def singleton_class(_cls=None, *, exc_cls=ValueError):
    instances = {}
    lock = Lock()

    def wrap(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            with lock:
                inst_ref = instances.get(cls)
                inst = inst_ref() if inst_ref else None
                if inst is None:
                    inst = cls(*args, **kwargs)
                    instances[cls] = weakref.ref(inst)
                    return inst
                raise exc_cls(f"An instance of {cls.__name__} already exists")
        return wrapper

    return wrap(_cls) if _cls else wrap
