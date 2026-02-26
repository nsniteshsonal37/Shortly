from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Link

router = APIRouter()


@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Short URL not found")
    link.clicks += 1
    db.commit()
    return RedirectResponse(url=link.original_url)