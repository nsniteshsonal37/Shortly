from fastapi import FastAPI
from app.api.routes_auth import router as auth_router
from app.db.database import engine, Base
import time
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Shortly Auth Service")

Instrumentator().instrument(app).expose(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://100.83.168.130:5173",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
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
