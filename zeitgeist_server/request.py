class Request:
    def __init__(self,
                 headers=None,
                 content_type=None,
                 body=None,
                 method=None,
                 target=None):
        self.content_type = content_type
        self.headers = headers
        self.body = body
        self.method = method
        self.target = target
