from webob.request import Request
from http import HTTPStatus


class ResponseError(Exception):
    def __init__(self, message: str, http_status: HTTPStatus):
        self.message = message
        self.http_status = http_status
        super().__init__(self.message)


class MethodNotAllowed(ResponseError):
    def __init__(self, request: Request):
        message = f"{request.method} request is not allowed for {request.path}"
        super().__init__(message, HTTPStatus.METHOD_NOT_ALLOWED)