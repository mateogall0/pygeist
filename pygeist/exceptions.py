from pygeist.request import Request
from pygeist.utils.status_code import verify_status_code
import json


class ZeitgeistServerException(Exception):
    pass

class ServerAlreadyStarted(ZeitgeistServerException):
    pass

class SessionsStructureInit(ZeitgeistServerException):
    pass

class SessionsStructureDestruct(ZeitgeistServerException):
    pass

class SessionCreation(ZeitgeistServerException):
    pass

class EndpointsInit(ZeitgeistServerException):
    pass

class EndpointsDestruct(ZeitgeistServerException):
    pass

class ZEITException(ZeitgeistServerException):
    def __init__(self,
                 status_code: int,
                 detail: dict | str | None = '',
                 ) -> None:
        self.status_code = status_code
        self.detail = detail

    @property
    def status_code(self) -> int:
        return self._status_code

    @status_code.setter
    def status_code(self, status_code: int) -> None:
        verify_status_code(status_code)
        self._status_code = status_code

    def get_body_result(self):
        return self.detail

    def get_fres(self, server_version: str,req: Request) -> str:
        sres = self.detail if isinstance(self.detail, str) else json.dumps(self.detail)
        return (
            f"{server_version} {self.status_code} {req.rid}\r\n"
            f"Content-Length: {len(sres)}\r\n\r\n"
            f"{sres}"
        )
