class HTTPRequest:
    def __init__(self, method: str, host: str, body: bytes or None = None) -> None:
        self.method = method
        self.body = body
        pass

    def get_body(self) -> str:
        pass
