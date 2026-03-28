import re

from webob.request import Request

from roob.middlewares import Middleware


class TokenMiddleware(Middleware):
    _regex = re.compile(r"^Token: (\w+)$")

    def process_request(self, req: Request):
        header = req.headers.get("Authorization", "")
        match = self._regex.match(header)
        token = match and match.group(1) or None
        req.token = token