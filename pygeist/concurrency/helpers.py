import asyncio


job_queue = asyncio.Queue()


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
    asyncio.run(func(*ag, **kw))
    # job_queue.put_nowait((func, ag, kw))
