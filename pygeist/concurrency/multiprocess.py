from multiprocessing import Process, set_start_method
import sys
import signal
from typing import Callable
import platform


def multirunner(task: Callable,
                batch_size: int,
                args=()) -> None:
    processes = []
    for _ in range(batch_size):
        p = Process(target=task, daemon=False, args=args)
        p.start()
        processes.append(p)

    def shutdown(sig, frame):
        for p in processes:
            p.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for p in processes:
        p.join()

def fork_proc(runner, *ag):
    proc = Process(target=runner,
                   args=ag,
                   daemon=False)
    proc.start()
    return proc

def kill_proc(proc):
    if proc.is_alive():
        proc.terminate()
        proc.join()
