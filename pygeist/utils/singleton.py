import threading
from functools import wraps


def singleton_class(_cls=None, *, exc_cls=ValueError):
    """Decorator to make a class a singleton. Raises exc_cls if an instance already exists."""
    import threading
    lock = threading.Lock()
    instances = {}

    def decorator(cls):
        class SingletonWrapper(cls):
            def __new__(cls_inner, *args, **kwargs):
                with lock:
                    if cls in instances:
                        raise exc_cls(f"An instance of {cls.__name__} already exists.")
                    instance = super().__new__(cls_inner)
                    instances[cls] = instance
                    return instance

            @classmethod
            def _reset_instance(cls_inner):
                with lock:
                    instances.pop(cls, None)

        # preserve basic class info
        SingletonWrapper.__name__ = cls.__name__
        SingletonWrapper.__doc__ = cls.__doc__
        return SingletonWrapper

    if _cls is None:
        return decorator
    else:
        return decorator(_cls)
