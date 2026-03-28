from webob.request import Request

from core.constants import STATIC_TOKEN
from core.exceptions import UnauthorizedException


def login_required(handler):
    def wrapped_handler(request: Request, *args, **kwargs):
        if not request.token or request.token != STATIC_TOKEN:
            raise UnauthorizedException()
        return handler(request, *args, **kwargs)

    return wrapped_handler