from slowapi import Limiter
from fastapi import Request


def user_rate_limit_key(request: Request):
    """
    Identify clients by authenticated user ID.
    Fallback to IP if unauthenticated.
    """

    user = getattr(request.state, "user", None)

    if user:
        return f"user:{user['id']}"

    # fallback (public endpoints)
    return request.client.host


limiter = Limiter(key_func=user_rate_limit_key)