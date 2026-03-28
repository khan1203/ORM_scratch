from core.constants import STATIC_TOKEN
from core.models.token import Token


class AuthService:

    def get_auth_token(self, **kwargs) -> Token:
        return Token(token=STATIC_TOKEN)