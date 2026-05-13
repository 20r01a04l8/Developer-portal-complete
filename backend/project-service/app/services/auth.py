from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.models.user import User
from app.core.security import PasswordHasher
from app.core.jwt import JWTHandler
from app.core.exceptions import UnauthorizedException, ConflictException
from app.core.config import settings


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_data: UserCreate) -> User:
        if self.repository.email_exists(user_data.email):
            raise ConflictException(f"User with email '{user_data.email}' already exists")
        
        hashed_password = PasswordHasher.hash_password(user_data.password)
        
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hashed_password
        
        return self.repository.create(user_dict)

    def authenticate_user(self, credentials: UserLogin) -> TokenResponse:
        user = self.repository.get_active_user_by_email(credentials.email)
        
        if not user:
            raise UnauthorizedException("Invalid email or password")
        
        if not PasswordHasher.verify_password(credentials.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")
        
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
        
        access_token = JWTHandler.create_access_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60
        )

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repository.get(user_id)
        if not user:
            raise UnauthorizedException("User not found")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_by_email(email)
        if not user:
            raise UnauthorizedException("User not found")
        return user
