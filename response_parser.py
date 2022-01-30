from typing import TypedDict


class HttpResponse(TypedDict):
    status_code: int
    headers: dict[str, str]
    body: str or None

def parse_http_response(response: str) -> HttpResponse:
    headers_and_body = response.split('\r\n\r\n')
    if len(headers_and_body) < 1:
        # TODO
        raise Exception()
    
    headers = headers_and_body[0]
    body = headers_and_body[1] if len(headers_and_body) == 2 else None

    status_line = headers[0]
    remaining_headers = headers[1:]
    
    return {
        'status_code': 0,
        'headers': remaining_headers,
        'body': body,
    }
