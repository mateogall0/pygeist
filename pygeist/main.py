import argparse
import importlib
from pygeist import ZeitgeistAPI
from multiprocessing import Process
from time import sleep
import sys
import signal


def main():
    parser = argparse.ArgumentParser('pygeist',
                                     description="Pygeist server runner")

    parser.add_argument(
        "app",
        help="Module:app format (e.g. myapp:app)"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=8000,
        help="Port number (default: 8000)"
    )
    parser.add_argument(
        "--workers", "-w", type=int, default=1,
        help="Number of process workers (default: 1)"
    )
    parser.add_argument(
        "--async-workers", type=int, default=4,
        help="Number of async workers (default: 4)"
    )

    args = parser.parse_args()
    app_value = args.app

    port = args.port
    workers = args.workers
    async_workers = args.async_workers

    module_name, app_name = app_value.split(":")

    def worker():
        module = importlib.import_module(module_name)
        app: ZeitgeistAPI = getattr(module, app_name)
        app.port = port
        app.workers = async_workers
        app.run()

    processes = []
    for _ in range(workers):
        p = Process(target=worker, daemon=True)
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
