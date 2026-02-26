from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

# Each request will use its own database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models (tables)
Base = declarative_base()


# Dependency (very important later)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()