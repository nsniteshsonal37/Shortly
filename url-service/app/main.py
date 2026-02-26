from fastapi import FastAPI
from app.api.routes_links import router as links_router
from app.api.routes_redirect import router as redirect_router
from app.db.database import engine, Base
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from app.core.rate_limiter import limiter
from app.core.auth_middleware import AuthContextMiddleware
import time

app = FastAPI(title="Shortly URL Service")
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


app.include_router(links_router)
app.include_router(redirect_router)