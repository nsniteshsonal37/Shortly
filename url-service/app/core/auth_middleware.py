from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.auth_client import verify_token


class AuthContextMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request.state.user = None

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                user = await verify_token(token)
                request.state.user = user
            except Exception:
                pass

        response = await call_next(request)
        return response