class Request:
    def __init__(self,
                 method=None,
                 target=None,
                 body=None,
                 headers=None,
                 ) -> None:
        self.headers = headers
        self.body = body
        self.method = method
        self.target = target
