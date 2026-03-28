#roob/framework.py

import os
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from webob import Request, Response
from whitenoise import WhiteNoise

from roob.middlewares import Middleware
from roob.routing_manager import RouteManager

class Roob:

    def __init__(self, template_dir: str = "templates", static_dir: str = "static"):
        self.routing_manager = RouteManager()

        # Initialize Jinja2 environment
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(template_dir))
        )

        # Initialize Whitenoise proxy
        self.whitenoise = WhiteNoise(application=self.wsgi_app, root=static_dir)

        self.exception_handler: Optional[callable] = None
        self.middleware = Middleware(app=self)


    # --------------------------------------------------------
    # WSGI Entry Point
    # --------------------------------------------------------

    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)


    def wsgi_app(self, environ, start_response):
        return self.middleware(environ, start_response)


    # --------------------------------------------------------
    # Request Handling
    # --------------------------------------------------------

    def handle_request(self, request: Request) -> Response:
        # Handle Requests that are not made for any static file
        try:
            return self.routing_manager.dispatch(request)

        except Exception as e:
            if not self.exception_handler:
                raise e

            return self.exception_handler(request, e)


    # --------------------------------------------------------
    # Routing System
    # --------------------------------------------------------

    def route(self, path: str, allowed_methods: Optional[list] = None):
        """Decorator to register route dynamically like Flask, FastAPI"""

        def decorator(handler):
            self.add_route(path, handler, allowed_methods)
            return handler

        return decorator


    def add_route(
        self,
        path: str,
        handler: callable,
        allowed_methods: Optional[list] = None
    ) -> None:
        """Django style explicit route registration."""

        self.routing_manager.register(path, handler, allowed_methods)


    # --------------------------------------------------------
    # Exception Handling
    # --------------------------------------------------------

    def add_exception_handler(self, handler: callable) -> None:
        self.exception_handler = handler


    # --------------------------------------------------------
    # Middleware System
    # --------------------------------------------------------

    def add_middleware(self, middleware_cls) -> None:
        self.middleware.add(middleware_cls)


    # --------------------------------------------------------
    # Template Rendering
    # --------------------------------------------------------

    def template(self, template_name: str, context: dict) -> str:

        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)