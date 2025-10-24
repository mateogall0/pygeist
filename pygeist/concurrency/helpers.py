import asyncio
import threading
import os

job_queue = asyncio.Queue()
_loop = None

async def worker():
    while True:
        func, args, kwargs = await job_queue.get()
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            print(f"Job failed: {e}")
        finally:
            job_queue.task_done()

def run_handler(func, *ag, **kw):
    global _loop
    asyncio.run_coroutine_threadsafe(job_queue.put((func, ag, kw)),
                                     _loop)

def enqueue_fd(fd, handler):
    return handler(fd)

def set_helper_loop(loop):
    global _loop
    _loop = loop
