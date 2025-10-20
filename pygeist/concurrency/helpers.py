import asyncio
import threading

# job_queue = asyncio.Queue()


# async def worker():
#     while True:
#         print('hi from worker')
#         func, args, kwargs = await job_queue.get()
#         print(func, args, kwargs)
#         try:
#             result = await func(*args, **kwargs)
#             print(result)
#         except Exception as e:
#             print(f"Job failed: {e}")
#         finally:
#             job_queue.task_done()

def run_handler(func, *ag, **kw):
    asyncio.run(func(*ag, **kw))
    return

def enqueue_fd(fd, handler):
    threading.Thread(target=handler, args=(fd,), daemon=False).start()
