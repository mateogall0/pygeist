import asyncio


job_queue = asyncio.Queue()


async def worker():
    while True:
        print('hi from worker')
        func, args, kwargs = await job_queue.get()
        print(func, args, kwargs)
        try:
            result = await func(*args, **kwargs)
            print(result)
        except Exception as e:
            print(f"Job failed: {e}")
        finally:
            job_queue.task_done()

def run_handler(func, *ag, **kw):
    asyncio.run(func(*ag, **kw))
    return

def enqueue_fd(fd, handler):
    print(handler)
    print(fd)
    handler(fd)
    print('finished handler')
    return
    print('enqueuing')

    job_queue.put_nowait((handler, (fd,), {}))
    return
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(job_queue.put((handler, (fd,), {})), loop)
    print('finished enqueugin')
