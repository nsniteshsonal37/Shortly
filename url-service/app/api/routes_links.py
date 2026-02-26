from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.db.models import Link
from app.core.deps import get_current_user
from app.db.database import get_db
from app.schemas.link_schema import LinkCreate, LinkResponse
from app.services.link_service import create_link,  get_user_links, delete_link
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/links", tags=["Links"])


@router.post("/", response_model=LinkResponse)
@limiter.limit("5/minute")
async def create_short_link(
    request: Request,
    link: LinkCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_link = create_link(
        db=db,
        original_url=str(link.original_url),
        owner_id=current_user["id"]
    )
    return new_link


@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "You are authenticated!",
        "user": current_user
    }



@router.get("/", response_model=list[LinkResponse])
async def get_my_links(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    links = get_user_links(db, current_user["id"])
    return links



@router.delete("/{link_id}")
async def remove_link(
    link_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_link(db, link_id, current_user["id"])

    return {"message": "Link deleted successfully"}