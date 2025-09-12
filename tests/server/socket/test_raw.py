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
                             ('this', 'is', 'invalid', b'400 Bad request'),
                         ])
def test_server_socket_request(example_server, method_str, target, body, expected):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", example_server))
        s.sendall(f"{method_str} {target}\r\n\r\n{body}".encode())
        data = s.recv(1024)
        assert data == expected

@pytest.mark.parametrize("method_str,target,body,expected",
                         [
                             ("POST", "/post-broadcast", "hello there", b"sending stuff"),
                             ("POST", "/post-broadcast", " ", b"sending stuff"),
                         ])
def test_server_unwanted(example_server, method_str, target, body, expected):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s0, \
         socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:

        s0.connect(("127.0.0.1", example_server))
        s0.sendall(f"{method_str} {target}\r\n\r\n{body}".encode())
        data = s0.recv(1024)
        assert data == expected

        s1.connect(("127.0.0.1", example_server))

        s1.sendall(f"{method_str} {target}\r\n\r\n{body}".encode())
        data = s1.recv(1024)
        assert data == expected

        data = s0.recv(1024)
        assert data == body.encode()
