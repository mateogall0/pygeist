import asyncio


def run_handler(func, *args, **kwargs):
    if asyncio.iscoroutinefunction(func):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        coro = func(*args, **kwargs)

        if loop and loop.is_running():
            loop.create_task(coro)
        else:
            asyncio.run(coro)
        return None
    return func(*args, **kwargs)
