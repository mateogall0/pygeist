from pygeist.abstract.methods_handler import AAsyncMethodsHandler
import multiprocessing
import socket
import time
import json
import weakref
import asyncio
import threading
from typing import Union, Optional

def _runner(app):
    app.run()


class Response:
    def __init__(self,
                 raw_payload: bytes,
                 _process=True,
                 ) -> None:
        self.payload = raw_payload.decode()
        if not _process:
            return
        all_headers, _, content = self.payload.partition("\r\n\r\n")
        self.status_code = int(all_headers.split()[1])
        self.all_head = all_headers
        self.content = content
        self.body = content

    @property
    def body(self) -> Optional[Union[dict, str]]:
        return self._body

    @body.setter
    def body(self, body: Optional[Union[dict, str]]) -> None:
        try:
            self._body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            self._body = body

    def __str__(self) -> str:
        return f'Response:\npayload: {self.payload}\n'

    __repr__ = __str__


class TestClient(AAsyncMethodsHandler):
    __test__ = False  # tells pytest to not collect this

    def __init__(self,
                 app,
                 buff_size=8192,
                 create_server=True,
                 ) -> None:
        self.app = app
        self.buff_size = buff_size
        self.reader = None
        self.writer = None
        self.create_server = create_server

        if not self.create_server:
            return

        self.server_process = multiprocessing.Process(target=_runner,
                                                      args=(self.app,),
                                                      daemon=True,)
        self.server_process.start()

        for _ in range(500):
            try:
                with socket.create_connection(("127.0.0.1",
                                               self.app.port),
                                              timeout=0.1):
                    break
            except OSError:
                time.sleep(0.001)
        else:
            raise RuntimeError("server did not start in time")

        self._finalizer = weakref.finalize(self, self._cleanup_server, self.server_process)

    async def _method_handler(self,
                              *ag,
                              **kw,
                              ) -> Response:
        return await self.send_receive(*ag, **kw)

    async def link(self):
        reader, writer = await asyncio.open_connection("localhost",
                                                       self.app.port)
        self.reader = reader
        self.writer = writer

    async def send_receive(self,
                           method: str,
                           target: str,
                           headers: dict = {},
                           _process=True,
                           data='',
                           ) -> Response:
        headers_str = ''.join(f'\r\n{k}: {v}' for k, v in headers.items())
        if isinstance(data, dict):
            data = json.dumps(data)
        payload = f"{method.upper()} {target}{headers_str}\r\n\r\n{data}".encode()
        self.writer.write(payload)
        await self.writer.drain()
        print('testclient now waiting for response...')
        response_data = await self.reader.read(self.buff_size)
        return Response(response_data, _process)

    async def unlink(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.writer = None
            self.reader = None

    @staticmethod
    def _cleanup_server(proc):
        if proc.is_alive():
            proc.terminate()
            proc.join()

    def stop_server(self):
        if not self.create_server:
            return
        self._cleanup_server(self.server_process)
        self._finalizer.detach()

    def __del__(self):
        self.stop_server()
