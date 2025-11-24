from abc import ABC


class ARequest(ABC):
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
