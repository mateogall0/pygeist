import asyncio
import time
import threading

# Background queue and loop
_task_queue = asyncio.Queue()
started = threading.Event()

def _loop_runner(loop, queue):
    asyncio.set_event_loop(loop)

    async def worker():
        while True:
            coro = await queue.get()
            task = asyncio.create_task(coro)
            await asyncio.sleep(0)  # allow scheduled tasks to run
            queue.task_done()
    loop.create_task(worker())
    loop.run_forever()

# Start background loop in a thread
_bg_loop = asyncio.new_event_loop()
threading.Thread(target=_loop_runner, args=(_bg_loop, _task_queue), daemon=True).start()

def push_async(coro):
    """Fire-and-forget: push coroutine to background loop, do not wait."""
    _bg_loop.call_soon_threadsafe(_task_queue.put_nowait, coro)
    time.sleep(0)
