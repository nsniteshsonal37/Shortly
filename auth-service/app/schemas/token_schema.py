from pydantic import BaseModel


# what another service sends to auth-service
class TokenVerifyRequest(BaseModel):
    token: str


# what auth-service returns
class TokenVerifyResponse(BaseModel):
    id: int
    email: str
    username: str