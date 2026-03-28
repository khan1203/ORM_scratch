from typing import Optional
from webob import Request

from roob.utils.route_helper import RoutingHelper
from roob.models.route_definition import RouteDefinition


class RouteManager:
    def __init__(self):
        self.routes = {}

    def register(self, path, handler, allowed_methods: Optional[list] = None):
        if allowed_methods:
            allowed_methods = [method.upper() for method in allowed_methods]
        if path in self.routes:
            raise RuntimeError(f"Path: {path} already bind to another handler")
        self.routes[path] = RouteDefinition(handler, allowed_methods)

    def dispatch(self, http_request: Request):
        # handler, kwargs = RoutingHelper.get_handler(self.routes, http_request)
        # return handler(http_request, **kwargs)
        route_def: RouteDefinition = RoutingHelper.get_route_definition(self.routes, http_request)
        return route_def.handler(http_request, **route_def.kwargs)