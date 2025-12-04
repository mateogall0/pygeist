import asyncio
import threading
import os


class WorkersQueue:
    def __init__(self) -> None:
        self.job_queue = None
        self.loop = None
        self.start = False


    def init(self, loop: asyncio.AbstractEventLoop):
        if self.start is True:
            raise RuntimeError('workers queue already initialized')
        self.loop = loop
        self.job_queue = asyncio.Queue()
        self.start = True

    async def worker(self,):
        while True:
            func, args, kwargs = await self.job_queue.get()
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                print(f"Job failed: {e}")
            finally:
                self.job_queue.task_done()

    def run_handler(self, func, *ag, **kw):
        self.loop.call_soon_threadsafe(
            lambda: self.job_queue.put_nowait((func, ag, kw))
        )

workers_queue = WorkersQueue()
