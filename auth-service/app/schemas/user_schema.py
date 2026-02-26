from pydantic import BaseModel, EmailStr


# Request body for registering a user
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


# Request body for login
class UserLogin(BaseModel):
    identifier: str
    password: str


# Response model (what login returns)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"