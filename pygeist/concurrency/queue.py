import asyncio
import threading


_task_queue = asyncio.Queue()
_bg_loop = asyncio.new_event_loop()

def _loop_runner(loop, queue):
    asyncio.set_event_loop(loop)

    async def worker():
        while True:
            coro = await queue.get()
            # schedule the task
            loop.create_task(coro)
            queue.task_done()

    loop.create_task(worker())
    loop.run_forever()

threading.Thread(target=_loop_runner, args=(_bg_loop, _task_queue), daemon=True).start()

def push_async(coro):
    """Fire-and-forget: push coroutine to background loop, but ensure it's queued."""
    fut = asyncio.run_coroutine_threadsafe(_task_queue.put(coro), _bg_loop)
    fut.result()
