import asyncio
import threading
import os

job_queue = asyncio.Queue()


async def worker():
    while True:
        await asyncio.sleep(0.01)
        func, args, kwargs = await job_queue.get()
        print(func, args, kwargs)
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            print(f"Job failed: {e}")
        finally:
            job_queue.task_done()

def run_handler(func, *ag, **kw):
    job_queue.put_nowait((func, ag, kw))

def enqueue_fd(fd, handler):
    return handler(fd)
    threading.Thread(target=handler, args=(fd,), daemon=False).start()
