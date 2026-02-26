from fastapi import FastAPI
from app.api.routes_auth import router as auth_router
from app.db.database import engine, Base
import time

app = FastAPI(title="Shortly Auth Service")



@app.get("/")
def root():
    return {"message": "Shortly Auth Service is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)