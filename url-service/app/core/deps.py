from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth_client import verify_token

# FastAPI will require: Authorization: Bearer <token>
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Extract token from request and verify it using auth-service
    """

    token = credentials.credentials

    try:
        user_data = await verify_token(token)
    except HTTPException:
        raise

    return user_data