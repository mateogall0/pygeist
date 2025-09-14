from functools import wraps
from threading import Lock


def singleton_class(_cls=None, *, exc_cls=ValueError):
    """
    Decorator that restricts a class to a single instance.
    Raises `exc_cls` if an instance already exists.
    """
    instances = {}
    lock = Lock()

    def wrap(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
                    return instances[cls]
                raise exc_cls(f"An instance of {cls.__name__} already exists")
        return wrapper

    if _cls is None:
        # decorator called with arguments
        return wrap
    else:
        # decorator called without arguments
        return wrap(_cls)
