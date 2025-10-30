from urllib import parse
import json


class Request:
    def __init__(self,
                 method=None,
                 target=None,
                 body=None,
                 headers=None,
                 client_key=None,
                 query_params=None,
                 rid=None,
                 ) -> None:
        self.headers = headers
        self.body = body
        self.method = method
        self.target = target
        self.client_key = client_key
        self.query_params = query_params
        self.rid = rid

    @property
    def query_params(self) -> dict:
        return self._query_params

    @query_params.setter
    def query_params(self, params: str | None) -> None:
        self._query_params = parse.parse_qs(params)

    @property
    def body(self) -> str | dict | None:
        return self._body

    @body.setter
    def body(self, body: str | None) -> None:
        try:
            self._body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            self._body = body
