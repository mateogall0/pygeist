class Request:
    def __init__(self,
                 method=None,
                 target=None,
                 body=None,
                 headers=None,
                 client_key=None,
                 ) -> None:
        self.headers = headers
        self.body = body
        self.method = method
        self.target = target
        self.client_key = client_key
