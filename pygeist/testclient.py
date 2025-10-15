from pygeist.zeitgeist import ZeitgeistAPI
from pygeist.abstract.methods_handler import AMethodsHandler
import multiprocessing
import socket
import time
import json


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
        self.all_head = all_headers
        self.content = content
        self.body = content

    @property
    def body(self) -> dict | str | None:
        return self._body

    @body.setter
    def body(self, body: dict | str | None) -> None:
        try:
            self._body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            self._body = body

    def __str__(self) -> str:
        return f'Response:\npayload: {self.payload}\n'

    def __repr__(self) -> str:
        return str(self)

class TestClient(AMethodsHandler):
    __test__ = False  # tells pytest to not collect this

    def __init__(self,
                 app: ZeitgeistAPI,
                 buff_size=8192,
                 ) -> None:
        self.app = app
        self.buff_size = buff_size
        self.sock = None
        self.server_process = multiprocessing.Process(target=_runner,
                                                 args=(self.app,))
        self.server_process.start()

        for _ in range(50):
            try:
                with socket.create_connection(("127.0.0.1",
                                               self.app.port),
                                              timeout=0.1):
                    break
            except OSError:
                time.sleep(0.001)
        else:
            raise RuntimeError("server did not start in time")

    def _method_handler(self,
                        *ag,
                        **kw,
                        ) -> Response:
        return self.send_receive(*ag, **kw)

    def link(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", self.app.port))

    def send_receive(self,
                     method: str,
                     target: str,
                     headers: dict = {},
                     _process=True,
                     data='') -> Response:
        headers_str = ''.join(f'\r\n{k}: {v}' for k, v in headers.items())
        payload = f"{method.upper()} {target}{headers_str}\r\n\r\n{data}".encode()
        self.sock.sendall(payload)
        response_data = self.sock.recv(self.buff_size)
        return Response(response_data, _process)

    def unlink(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def __del__(self):
        self.server_process.terminate()
        self.server_process.join()
