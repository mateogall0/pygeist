import asyncio
import threading
import os


class WorkersQueue:
    def __init__(self) -> None:
        self.job_queue = None
        self.loop = None

    def init(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        self.job_queue = asyncio.Queue()

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
        asyncio.run_coroutine_threadsafe(
            self.job_queue.put((func, ag, kw)),
            self.loop,
        )

workers_queue = WorkersQueue()
