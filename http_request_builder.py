def build_http_request(method: str, path: str, host: str, extra_headers=[], body: str = "") -> str:
    """
    Returns a valid HTTP request from the given parameters.

    Parameters:
    - `method` - valid HTTP methods (e.g. "POST" or "GET")
    - `path` - the path part of a URL (e.g. "/" or "/index.html")
    - `host` - the host of the endpoint (e.g. "google.com" or "ualberta.ca")
    - `extra_headers` - an optional list of strings to be included as part
                        of the request headers (e.g. ["Content-Type": "application/json"])
    - `body` - the optional body of the request (if any)

    Returns:
    A string representation of a valid HTTP request
    """
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
