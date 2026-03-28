#roob/middlewares.py

import time
from typing import TYPE_CHECKING

from webob import Request
from webob.response import Response
from roob.exceptions import ResponseError

from roob.common_handlers import CommonHandlers
from roob.logger import create_logger

if TYPE_CHECKING:
    from roob.framework import Roob


#--------------------------------------------------
#                    Logger
#--------------------------------------------------

# logger = create_logger(__name__, level="DEBUG")
logger = create_logger(__name__)


#--------------------------------------------------
#                Base Middleware
#--------------------------------------------------

class Middleware:
    def __init__(self, app: "Roob"):
        self.app = app


    #--------------------------------------------------
    # WSGI Entry for Middleware
    #--------------------------------------------------
    def __call__(self, environ, start_response):
        http_request = Request(environ)
        response = self.handle_request(http_request)
        return response(environ, start_response)


    #--------------------------------------------------
    # Middleware Registration
    #--------------------------------------------------
    def add(self, middleware_cls) -> None:

        #v1.0
        """
        logger.debug(f"{middleware_cls.__name__}(app={self.app.__class__.__name__})")
        self.app = middleware_cls(app=self.app)
        """

        #v2.0
        logger.debug(f"Adding {middleware_cls.__name__}")

        # Create a new middleware instance that wraps the current app
        new_middleware = middleware_cls(app=self.app)

        # Replace the app with the new middleware chain
        self.app = new_middleware


    #--------------------------------------------------
    # Request Processing Hook
    #--------------------------------------------------
    def process_request(self, req: Request) -> None:
        logger.debug(f"{self.__class__.__name__}::process_request")


    #--------------------------------------------------
    # Response Processing Hook
    #--------------------------------------------------
    def process_response(self, req: Request, resp: Response) -> None:
        logger.debug(f"{self.__class__.__name__}::process_response")


    #--------------------------------------------------
    # Middleware Execution Pipeline
    #--------------------------------------------------
    def handle_request(self, request: Request) -> Response:
        self.process_request(request)

        if hasattr(self.app, "handle_request"):
            response = self.app.handle_request(request)
        else:
            response = self.app._handle_request(request)

        self.process_response(request, response)
        return response


#--------------------------------------------------
#              Error Handling Middleware
#--------------------------------------------------

class ErrorHandlerMiddleware(Middleware):

    def handle_request(self, request: Request) -> Response:
        try:
            return super().handle_request(request)
        except ValueError as e:
            return CommonHandlers.handle_value_error(request, e)
        except ResponseError as e:
            return CommonHandlers.handle_response_error(request, e)
        except Exception as e:
            return CommonHandlers.generic_exception_handler(request, e)


#--------------------------------------------------
#           Request / Response Logging Middleware
#--------------------------------------------------

class ReqResLoggingMiddleware(Middleware):

    def process_request(self, req: Request) -> None:
        super().process_request(req)
        logger.info("[%s] Requested URL: %s", req.method, req.path)


#--------------------------------------------------
#          Execution Time Measurement Middleware
#--------------------------------------------------

class ExecutionTimeMiddleware(Middleware):

    def process_request(self, req):
        super().process_request(req)
        req.start_time = time.time()


    def process_response(self, req, resp):
        super().process_response(req, resp)

        if hasattr(req, 'start_time'):
            duration = time.time() - req.start_time
            resp.headers['X-Response-Time'] = f"{duration:.4f}s"

            logger.info(f"Total Processing Time: {duration:.4f}")