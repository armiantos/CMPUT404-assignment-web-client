#!/usr/bin/env python3
# coding: utf-8
# Copyright 2022 Armianto Sumitro
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

from email import header
import sys
import socket
import re

# you may use urllib to encode data appropriately
import urllib.parse

from http_request_builder import build_http_request


def help():
    """
    Prints the usage of the CLI
    """
    print("httpclient.py [GET/POST] [URL]\n")


class HTTPResponse(object):
    def __init__(self, code: int = 200, body: str = ""):
        self.code = code
        self.body = body


STATUS_LINE_REGEX = re.compile(r"HTTP/\d\.\d (\d{3}) (.+)")


class InvalidHTTPResponseError(Exception):
    pass


class HTTPClient(object):
    def connect(self, host, port):
        """
        Initializes a socket connection to the given server
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def get_code(self, data: str) -> int:
        """
        Returns the integer status code given a full HTTP response
        """
        status_line = data.split('\r\n')[0]
        matches = STATUS_LINE_REGEX.match(status_line)
        if matches is None:
            raise InvalidHTTPResponseError
        return int(matches.group(1))

    def get_headers(self, data: str):
        """
        Returns a dictionary of headers (excluding the status line) given a full HTTP response.
        Header values are of type string.
        """
        headers = data.split('\r\n\r\n')[0]
        non_status_line_headers = headers[1:]
        formatted_headers = {}
        for header in non_status_line_headers:
            key, value = header.split(": ")
            formatted_headers[key] = value
        return formatted_headers

    def get_body(self, data):
        """
        Returns the body of an HTTP response if there is any, None otherwise.
        """
        headers_and_body = data.split('\r\n\r\n')
        if len(headers_and_body) < 2:
            return None
        return headers_and_body[1]

    def sendall(self, data):
        """
        Sends a string or a bytes like object down the socket
        """
        self.socket.sendall(data.encode("utf-8"))

    def close(self):
        """
        Closes the socket connetion
        """
        self.socket.close()

    def recvall(self, sock: socket.SocketType):
        """
        Returns the server response encoded as a utf-8 string. Blocks if the socket is not closed properly.
        """
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        """
        Performs an HTTP GET to the given url.

        Params:
        - `url` - the endpoint to GET from

        Returns:
        An HTTPResponse object
        """
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme != "http":
            raise Exception()

        host_ip = socket.gethostbyname(parsed_url.hostname)
        port = parsed_url.port or 80
        path = parsed_url.path or "/"
        if len(parsed_url.query) > 0:
            path += f"?{parsed_url.query}"

        self.connect(host_ip, port)
        http_request = build_http_request(method="GET", path=path, host=parsed_url.hostname)
        self.sendall(http_request)
        self.socket.shutdown(socket.SHUT_WR)  # Prevent further sends to server
        http_response = self.recvall(self.socket)
        self.close()

        code = self.get_code(http_response)
        body = self.get_body(http_response)
        return HTTPResponse(code, body)

    def POST(self, url: str, args=None):
        """
        Performs an HTTP POST to the given url.

        Params:
        - `url` - the endpoint to POST to
        - `args` - a dictionary mapping keys to string values that will be URL encoded as the POST body

        Returns:
        An HTTPResponse object
        """
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme != "http":
            raise Exception()

        host_ip = socket.gethostbyname(parsed_url.hostname)
        port = parsed_url.port or 80
        path = parsed_url.path or "/"
        if len(parsed_url.query) > 0:
            path += f"?{parsed_url.query}"

        # Encode form fields
        request_body = ""
        if args is not None:
            safe_fields = [
                f"{urllib.parse.quote_plus(key)}={urllib.parse.quote_plus(value)}" for key,
                value in args.items()]
            request_body = "&".join(safe_fields)

        self.connect(host_ip, port)
        http_request = build_http_request(
            method="POST",
            path=path,
            host=parsed_url.hostname,
            extra_headers=["Content-Type: application/x-www-form-urlencoded"],
            body=request_body,
        )
        self.sendall(http_request)
        self.socket.shutdown(socket.SHUT_WR)  # Prevent further sends to server
        http_response = self.recvall(self.socket)
        self.close()

        code = self.get_code(http_response)
        body = self.get_body(http_response)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        """
        Processes a GET/POST command
        """
        if command == "POST":
            return self.POST(url, args)
        else:
            return self.GET(url, args)


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if len(sys.argv) <= 1:
        help()
        sys.exit(1)
    elif len(sys.argv) == 3:
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
