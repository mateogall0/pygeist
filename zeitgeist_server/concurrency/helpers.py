from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

def submit_task(func, *args):
    executor.submit(func, *args)
