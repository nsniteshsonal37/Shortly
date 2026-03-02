from fastapi import FastAPI
from app.api.routes_links import router as links_router
from app.api.routes_redirect import router as redirect_router
from app.db.database import engine, Base
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from app.core.rate_limiter import limiter
from app.core.auth_middleware import AuthContextMiddleware
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI(title="Shortly URL Service")

Instrumentator().instrument(app).expose(app)

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

app.state.limiter = limiter
app.add_middleware(AuthContextMiddleware)
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Slow down."}
    )

@app.get("/")
def root():
    return {"message": "URL Service is running"}

@app.get("/test500")
def boom():
    raise Exception("500")


app.include_router(links_router)
app.include_router(redirect_router)