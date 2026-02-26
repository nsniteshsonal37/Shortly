from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.models import User
from app.core.security import hash_password, verify_password


def create_user(db: Session, email: str, username: str, password: str):
    # Hash the password before storing
    hashed_pw = hash_password(password)

    new_user = User(
        email=email,
        username=username,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, identifier: str, password: str):
    # determine if email or username
    user = db.query(User).filter(
        or_(
            User.email == identifier,
            User.username == identifier
        )
    ).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user