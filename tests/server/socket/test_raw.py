import socket
import pytest
from tests.fixtures.socket import example_server


@pytest.mark.parametrize("method_str,target,body,expected",
                         [
                             ('GET', '/get-1515', '', b'1515'),
                             ('GET', '/get-pow', 5, b'25'),
                             ('GET', '/get-pow', 0, b'0'),
                             ('GET', '/get-pow', '10', b'100'),
                             ('GET', '/get-pow', -10, b'100'),
                             ('GET', '/get-pow', 'something', b'error'),
                             ('GET', '/get-notnonexistent', '', b'404 Resource not found'),
                             ('POST', '/get-1515', '', b'405 Method not allowed'),
                         ])
def test_server_socket(example_server, method_str, target, body, expected):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", example_server))
        s.sendall(f"{method_str} {target}\r\n\r\n{body}".encode())
        data = s.recv(1024)
        assert data == expected
