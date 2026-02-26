from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserLogin, Token
from app.db.database import get_db
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token
from app.core.deps import get_current_user
from app.db.models import User

from app.schemas.token_schema import TokenVerifyRequest, TokenVerifyResponse
from jose import jwt, JWTError
import os

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.email, user.username, user.password)
    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username
    }


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.identifier, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token,
            "token_type":"bearer"}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }
    
@router.post("/verify", response_model=TokenVerifyResponse)
def verify_token(body: TokenVerifyRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            body.token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )
        user_email = payload.get("sub")

        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username
    }