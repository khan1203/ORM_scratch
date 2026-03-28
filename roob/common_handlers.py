import logging
from webob import Request, Response
from roob.constants import HttpStatus
from roob.exceptions import ResponseError

logger = logging.getLogger(__name__)


class CommonHandlers:
    @staticmethod
    def generic_exception_handler(request: Request, excp: Exception) -> Response:
        logger.exception(excp)
        response = {
            "message": f"Unhanded Exception Occurred: {str(excp)}"
        }
        return Response(
            json_body=response,
            status=HttpStatus.INTERNAL_SERVER_ERROR
        )
    @staticmethod
    def handle_value_error(request: Request, exc: ValueError) -> Response:
        logger.exception(exc)
        response = {
            "message": str(exc)
        }
        return Response(
            json_body=response,
            status=HttpStatus.BAD_REQUEST
        )

    @staticmethod
    def handle_response_error(request: Request, exc: ResponseError) -> Response:
        logger.exception(exc)
        response = {
            "message": exc.message
        }
        return Response(
            json_body=response,
            status=exc.http_status
        )

    @staticmethod
    def url_not_found_handler(request: Request) -> Response:
        response = {
            "message": f"Requested path: {request.path} does not exist"
        }
        return Response(
            json_body=response,
            status=HttpStatus.NOT_FOUND
        )
    @staticmethod
    def method_not_allowed_handler(request: Request) -> Response:
        response = {
            "message": f"{request.method} request is not allowed for {request.path}"
        }
        return Response(
            json_body=response,
            status=HttpStatus.METHOD_NOT_ALLOWED
        )