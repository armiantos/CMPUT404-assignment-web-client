def build_http_request(method: str, path: str, host: str, body: bytes or None = None) -> str:
    status_line = f"{method} {path} HTTP/1.1"
    headers = "\r\n".join(
        [
            f"Host: {host}",
        ]
    )
    return "\r\n".join([status_line, headers, "\r\n"])
