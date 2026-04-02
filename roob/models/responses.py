from typing import Any
from http import HTTPStatus
from webob.response import Response as BaseResponse

from roob.constants import ContentType
from roob.utils.common_utils import StatusUtils
from roob.utils.json_util import JSONUtils

class Response(BaseResponse):
    def __init__(self,status = HTTPStatus.OK, **kwargs):
        super().__init__(
            status=StatusUtils.to_str(status), 
            **kwargs
        )

class TextResponse(Response):
    def __init__(self, content: str, status: HTTPStatus = HTTPStatus.OK, **kwargs):
        super().__init__(
            text=content,
            status=status,
            content_type=ContentType.TEXT,
            **kwargs
        )


class JSONResponse(Response):
    def __init__(self, content: dict | Any, status: HTTPStatus = HTTPStatus.OK, **kwargs):
        super().__init__(
            json=JSONUtils.to_dict(content),
            status=status,
            content_type=ContentType.JSON,
            **kwargs
        )


class HTMLResponse(Response):
    def __init__(self, content: str, status: HTTPStatus= HTTPStatus.OK, **kwargs):
        super().__init__(
            body=content,
            status=status,
            content_type=ContentType.HTML,
            **kwargs
        )