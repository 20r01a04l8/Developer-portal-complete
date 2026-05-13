from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware
from app.api.health import router as health_router
from app.api.tasks import router as tasks_router
from app.core.exceptions import BaseAPIException
from app.core.exception_handlers import (
    api_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

setup_cors(app)
app.add_middleware(LoggingMiddleware)

app.add_exception_handler(BaseAPIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(health_router, prefix=settings.api_prefix, tags=["health"])
app.include_router(tasks_router, prefix=f"{settings.api_prefix}/tasks", tags=["tasks"])
