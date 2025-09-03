from zeitgeist_server.exceptions import ServerAlreadyStarted

def singleton_class(cls):
    """
    Decorator that restricts classes of having more than one instance
    """
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            inst = cls(*args, **kwargs)
            instances[cls] = inst
            return inst
        raise ServerAlreadyStarted('server already initialized')
    return wrapper
