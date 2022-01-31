def build_http_request(
    method: str, path: str, host: str, extra_headers: list[str] = [], body: str or None = None
) -> str:
    status_line = f"{method} {path} HTTP/1.1"
    headers = [
        f"Host: {host}",
    ]
    if len(extra_headers) > 0:
        headers.extend(extra_headers)

    payload = "\r\n"
    if body != None:
        payload += body
        headers.append(f"Content-Length: {len(body)}")

    request_body = "\r\n".join([status_line, "\r\n".join(headers), payload])
    return request_body
