from urllib import parse
import json
from pygeist.abstract.request import ARequest


class Request(ARequest):
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
