import secrets
from typing import Any, Dict

from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from src.core.config import settings

users: Dict[str, Dict[str, Any]] = {
    'admin@ateliedigital.com': {
        'name': settings.NAME_ADMIN,
        'avatar': None,
        'roles': ['read'],
        'password': settings.PASSWORD_ADMIN,
    },
}


class MyAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            raise FormValidationError({
                'username': 'O nome de usuário deve conter pelo menos 3 caracteres'
            })

        user = users.get(username)

        if user and secrets.compare_digest(user['password'], password):
            request.session.update({'username': username})
            return response

        raise LoginFailed('Usuário ou senha inválidos')

    async def is_authenticated(self, request: Request) -> bool:
        username = request.session.get('username')
        user = users.get(username) if username else None

        if user:
            request.state.user = user
            return True

        return False

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
