from webob.request import Request

from core import app
from core.models.token import Token
from core.service.auth_service import AuthService
from roob.models.responses import JSONResponse

service = AuthService()


@app.route('/token', allowed_methods=["POST"])
def get_token(request: Request) -> JSONResponse:
    token: Token = service.get_auth_token(**request.json)
    return JSONResponse(token._asdict())