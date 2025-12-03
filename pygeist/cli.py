import argparse
import importlib
from pygeist.concurrency.multiprocess import multirunner

class AlignedFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, max_help_position=48, **kwargs)

def worker(
    module_name: str,
    app_name: str,
    async_workers: int,
    port: int,
) -> None:
    module = importlib.import_module(module_name)
    app = getattr(module, app_name)
    app.workers = async_workers
    app.port = port
    app.run()

def main():
    parser = argparse.ArgumentParser(
        'pygeist',
        description="Pygeist server runner",
        formatter_class=AlignedFormatter,
    )

    parser.add_argument(
        "app",
        help="Module:app format (e.g. myapp:app)"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=4000,
        help="Port number (default: 4000)"
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
    workers = args.workers
    port = args.port
    async_workers = args.async_workers
    module_name, app_name = app_value.split(":")

    print(f'Starting server on port {port}...')
    print('press Ctrl+C to stop it')
    multirunner(
        worker,
        workers,
        (module_name,
         app_name,
         async_workers,
         port,)
    )
    print('\nstopped')
