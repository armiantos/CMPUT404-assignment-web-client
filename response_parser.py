from typing import TypedDict


class HttpResponse(TypedDict):
    status_code: int
    headers: dict[str, str]
    body: str or None


class IncompleteHttpResponseError(Exception):
    pass


def parse_http_response(response: str) -> HttpResponse:
    """
    Parses the string decoded HTTP payload and returns a structured response object.

    Params:
    - `response` - the string decoded HTTP payload

    Returns:
    a dictionary with the following fields:
    - `status_code` - the HTTP status code (e.g. 200 if the response was a success)
    - `headers` - a key, value pair dictionary of all the headers (e.g. 'Content-Length': '100')
    - `body` - the body of the response decoded as utf-8
    """
    headers_and_body = response.split("\r\n\r\n")
    if len(headers_and_body) < 1:
        # TODO
        raise IncompleteHttpResponseError()

    headers = headers_and_body[0].split("\r\n")
    body = headers_and_body[1] if len(headers_and_body) == 2 else None

    status_line = headers[0]

    remaining_headers = headers[1:]
    formatted_headers = {}
    for header in remaining_headers:
        key, value = header.split(": ")
        formatted_headers[key] = value

    return {
        "status_code": 0,
        "headers": formatted_headers,
        "body": body,
    }
