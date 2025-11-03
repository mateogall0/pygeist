import pytest
import asyncio
from tests.fixtures.socket import example_server
from tests.fixtures.routed import example_routed_server


@pytest.mark.asyncio
@pytest.mark.parametrize("method_str,target,body,expected",
                         [
                             ('GET', '/get-1515', '', b'1515'),
                             ('GET', '/get-pow', 5, b'25'),
                             ('GET', '/get-pow', 0, b'0'),
                             ('GET', '/get-pow', 10, b'100'),
                             ('GET', '/get-pow', -10, b'100'),
                             ('GET', '/get-pow', 'something', b'error'),
                         ])
async def test_server_socket_request_async(example_server, method_str, target, body, expected):
    reader, writer = await asyncio.open_connection("localhost", example_server)
    writer.write(f"{method_str} {target}\r\n\r\n{body}".encode())
    await writer.drain()

    data = await reader.read(1024)
    assert data == expected

    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
@pytest.mark.parametrize("method_str,target,body,expected",
                         [
                             ('GET', '/get-1515', '', '1515'),
                             ('GET', '/get-pow', 5, '25'),
                             ('GET', '/get-pow', 'something', 'error'),
                         ])
async def test_server_socket_request_routed_async(example_routed_server, method_str, target, body, expected):
    reader, writer = await asyncio.open_connection("localhost", example_routed_server)
    writer.write(f"{method_str} {target}\r\n\r\n{body}".encode())
    await writer.drain()

    data = await reader.read(1024)
    _, _, after = data.decode().partition("\r\n\r\n")
    assert after == expected

    writer.close()
    await writer.wait_closed()
