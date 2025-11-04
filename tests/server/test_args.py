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
