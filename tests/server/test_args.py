import subprocess
import time
import socket
import pytest
from tests.fixtures.routed import _find_free_port
from pygeist import TestClient


def test_cli_module_not_found():
    port = _find_free_port()
    cmd = ["python", "-m", "pygeist",
           "nonexistent.directory:app",
           "--workers", "2"]
    proc = subprocess.Popen(cmd)
    for _ in range(1000):
        try:
            with socket.create_connection(("127.0.0.1",
                                           port),
                                          timeout=0.1):
                raise RuntimeError('server did start')
        except OSError:
            time.sleep(0.001)

    proc.terminate()
    proc.wait()

    # even if the module is not found the exit code is zero
    assert proc.returncode == 0

@pytest.mark.parametrize(
    "batch_size",
    [str(i) for i in range(1, 5)]
)
def test_cli_runs_basic(batch_size: str):
    port = _find_free_port()
    cmd = ["python", "-m", "pygeist",
           "examples.basic.intro:app",
           "-p", str(port),
           "--workers", batch_size,]
    proc = subprocess.Popen(cmd)

    for _ in range(1000):
        try:
            with socket.create_connection(("127.0.0.1",
                                           port),
                                          timeout=0.1):
                break
        except OSError:
            time.sleep(0.001)
    else:
        raise RuntimeError("server did not start in time")

    proc.terminate()
    proc.wait()
    assert proc.returncode == 0

@pytest.mark.parametrize(
    "batch_size, clients_count",
    [
        (1, 512),
        (2, 1024),
        (3, 2048),
    ],
)
@pytest.mark.asyncio
async def test_cli_brute_basic(batch_size: int, clients_count: int):
    port = _find_free_port()
    cmd = ["python", "-m", "pygeist",
           "examples.basic.intro:app",
           "-p", str(port),
           "--workers", str(batch_size),]
    proc = subprocess.Popen(cmd)

    for _ in range(1000):
        try:
            with socket.create_connection(("127.0.0.1",
                                           port),
                                          timeout=0.1):
                break
        except OSError:
            time.sleep(0.001)
    else:
        raise RuntimeError("server did not start in time")

    clients = []
    for _ in range(clients_count):
        c = TestClient(None, create_server=False)
        await c.link(port=port)

    for c in clients:
        res = await c.get('/')
        assert res.status_code == 200

    for c in clients:
        await c.unlink()

    proc.terminate()
    proc.wait()
    assert proc.returncode == 0
