from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime
from app.db.database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)

    original_url = Column(String, nullable=False)

    short_code = Column(String(10), unique=True, index=True, nullable=False)

    owner_id = Column(Integer, index=True, nullable=False)

    clicks = Column(Integer, default=0)   # 👈 NEW FIELD

    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint("owner_id", "original_url", name="uix_owner_url"),
    )