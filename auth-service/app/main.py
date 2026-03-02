from fastapi import FastAPI
from app.api.routes_auth import router as auth_router
from app.db.database import engine, Base
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Shortly Auth Service")

origins = [
    "http://localhost:5173",  # Vite frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Shortly Auth Service is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)