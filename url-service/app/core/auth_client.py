import os
import httpx
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")


async def verify_token(token: str):
    """
    Calls the auth-service to verify a JWT token
    """

    url = f"{AUTH_SERVICE_URL}/auth/verify"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json={"token": token},
                timeout=5.0
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service unreachable"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return response.json()