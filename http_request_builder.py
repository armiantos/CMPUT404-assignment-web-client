def build_http_request(method: str, path: str, host: str, extra_headers=[], body: str = "") -> str:
    status_line = f"{method} {path} HTTP/1.1"
    headers = [
        f"Host: {host}",
        "Connection: close"
    ]
    if len(extra_headers) > 0:
        headers.extend(extra_headers)

    payload = "\r\n"
    if len(body) > 0 or method == "POST":
        payload += body
        headers.append(f"Content-Length: {len(body)}")

    request_body = "\r\n".join([status_line, "\r\n".join(headers), payload])
    return request_body
