from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes.gateway import router as gateway_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API Gateway - Single entry point for all microservices"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gateway_router, prefix=settings.api_prefix)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": settings.app_version
    }
