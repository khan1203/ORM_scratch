from typing import Any

from webob.response import Response

from roob.constants import HttpStatus, ContentType
from roob.utils.json_util import JSONUtils


class TextResponse(Response):
    def __init__(self, content: str, status: str = HttpStatus.OK, **kwargs):
        super().__init__(
            text=content,
            status=status,
            content_type=ContentType.TEXT,
            **kwargs
        )


class JSONResponse(Response):
    def __init__(self, content: dict | Any, status: str = HttpStatus.OK, **kwargs):
        super().__init__(
            json=JSONUtils.to_dict(content),
            status=status,
            content_type=ContentType.JSON,
            **kwargs
        )


class HTMLResponse(Response):
    def __init__(self, content: str, status: str = HttpStatus.OK, **kwargs):
        super().__init__(
            body=content,
            status=status,
            content_type=ContentType.HTML,
            **kwargs
        )