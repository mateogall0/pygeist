from multiprocessing import Process
import sys
import signal
from typing import Callable


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
