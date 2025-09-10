class Request:
    def __init__(self,
                 method=None,
                 target=None,
                 body=None,
                 headers=None,
                 content_type=None,
                 ) -> None:
        self.content_type = content_type
        self.headers = headers
        self.body = body
        self.method = method
        self.target = target
