from roob.constants import HttpStatus
from roob.exceptions import ResponseError


class ResourceNotFoundException(ResponseError):
    def __init__(self, message='Resource not found'):
        super().__init__(message, HttpStatus.METHOD_NOT_ALLOWED)


class UnauthorizedException(ResponseError):
    def __init__(self, message='You are not authorized to access this resource'):
        super().__init__(message, HttpStatus.UNAUTHORIZED)