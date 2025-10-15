import socket
import pytest
import time
from tests.fixtures.socket import example_server
from tests.fixtures.routed import example_routed_server


@pytest.mark.parametrize("method_str,target,body,expected",
                         [
                             ('GET', '/get-1515', '', b'1515'),
                             ('GET', '/get-pow', 5, b'25'),
                             ('GET', '/get-pow', 0, b'0'),
                             ('GET', '/get-pow', 10, b'100'),
                             ('GET', '/get-pow', -10, b'100'),
                             ('GET', '/get-pow', 'something', b'error'),
                             ('GET', '/get-notnonexistent', '', b'404 Resource not found'),
                             ('POST', '/get-1515', '', b'405 Method not allowed'),
                             ('this', 'is', 'invalid', b'400 Bad request'),
                         ])
def test_server_socket_request(example_server, method_str, target, body, expected):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", example_server))
        s.sendall(f"{method_str} {target}\r\n\r\n{body}".encode())

        data = s.recv(1024)
        assert data == expected

@pytest.mark.parametrize("method_str,target,body,expected",
                         [
                             ('GET', '/get-1515', '', '1515'),
                             ('GET', '/get-pow', 5, '25'),
                             ('GET', '/get-pow', 'something', 'error'),
                             ('GET', '/hello/get-hello', '', 'hello'),
                             ('GET', '/hello/bye/get-bye', '', 'bye'),
                         ])
def test_server_socket_request_routed(example_routed_server, method_str, target, body, expected):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", example_routed_server))
        s.sendall(f"{method_str} {target}\r\n\r\n{body}".encode())

        data = s.recv(1024)
        _, _, after = data.decode().partition("\r\n\r\n")
        assert after == expected
