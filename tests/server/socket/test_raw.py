import socket
import pytest
from tests.fixtures.socket import example_server


@pytest.mark.parametrize("target,body,expected",
                         [
                             ('/get-1515', '', b'1515'),
                             ('/get-pow', 5, b'25'),
                             ('/get-pow', 0, b'0'),
                             ('/get-pow', '10', b'100'),
                             ('/get-pow', -10, b'100'),
                             ('/get-pow', 'something', b'error'),
                         ])
def test_server_socket(example_server, target, body, expected):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", example_server))
        s.sendall(f"GET {target}\r\n\r\n{body}".encode())
        data = s.recv(1024)
        assert data == expected
