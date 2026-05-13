from fastapi import FastAPI
from app.core.config import settings
from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware
from app.api.health import router as health_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

setup_cors(app)
app.add_middleware(LoggingMiddleware)

app.include_router(health_router, prefix=settings.api_prefix, tags=["health"])
