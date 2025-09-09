import socket, time
from tests.fixtures.socket import example_server


def test_server_socket(example_server):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", example_server))
        s.sendall(b"GET /get-1515\r\n")
        data = s.recv(1024)
        assert data == b'1515'
