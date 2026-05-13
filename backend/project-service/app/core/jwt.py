from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from app.core.config import settings


class JWTHandler:
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
        
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    def verify_token(token: str) -> bool:
        payload = JWTHandler.decode_token(token)
        return payload is not None

    @staticmethod
    def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
        return JWTHandler.decode_token(token)
