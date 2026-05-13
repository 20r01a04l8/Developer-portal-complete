from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.core.auth import get_current_user, get_current_user_id
from app.core.logging import logger
from typing import Dict, Any

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repository = UserRepository(db)
    return AuthService(repository)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    logger.info(f"Registering user: {user_data.email}")
    user = service.register_user(user_data)
    logger.info(f"User registered with id: {user.id}")
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    service: AuthService = Depends(get_auth_service)
):
    logger.info(f"Login attempt for user: {credentials.email}")
    token = service.authenticate_user(credentials)
    logger.info(f"User logged in: {credentials.email}")
    return token


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    user_id: int = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service)
):
    logger.info(f"Fetching user info for id: {user_id}")
    user = service.get_user_by_id(user_id)
    return user


@router.get("/verify")
async def verify_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "valid": True,
        "user_id": current_user.get("sub"),
        "email": current_user.get("email"),
        "role": current_user.get("role")
    }
