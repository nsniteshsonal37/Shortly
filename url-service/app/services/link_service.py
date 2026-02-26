import random
import string
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import Link
from fastapi import HTTPException, status


def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_link(db: Session, original_url: str, owner_id: int):

    # 1️⃣ idempotency: same user + same URL
    existing = (
        db.query(Link)
        .filter(Link.owner_id == owner_id, Link.original_url == original_url)
        .first()
    )

    if existing:
        return existing

    # 2️⃣ collision-safe creation
    while True:
        code = generate_short_code()

        new_link = Link(
            original_url=original_url,
            short_code=code,
            owner_id=owner_id
        )

        try:
            db.add(new_link)
            db.commit()
            db.refresh(new_link)
            return new_link

        except IntegrityError:
            # database rejected duplicate short_code
            db.rollback()
            # try again with a new code

def get_user_links(db: Session, owner_id: int):
    return db.query(Link).filter(Link.owner_id == owner_id).all()


def delete_link(db: Session, link_id: int, owner_id: int):
    link = db.query(Link).filter(Link.id == link_id).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found!")

    # ownership check
    if link.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this link!"
        )

    db.delete(link)
    db.commit()

    return True