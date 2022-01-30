class HTTPRequest:
    def __init__(self, method: str, path: str, host: str, body: bytes or None = None) -> None:
        self.method = method
        self.path = path
        self.host = host
        self.body = body
        pass

    def get_body(self) -> str:
        status_line = f'{self.method} {self.path} HTTP/1.1'
        headers = '\r\n'.join([
            f'Host: {self.host}',
        ])
        return '\r\n'.join([status_line, headers, '\r\n'])
