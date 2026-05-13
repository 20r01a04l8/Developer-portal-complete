from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from app.core.jwt import JWTHandler
from app.core.exceptions import UnauthorizedException

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    token = credentials.credentials
    
    payload = JWTHandler.get_token_payload(token)
    
    if payload is None:
        raise UnauthorizedException("Invalid or expired token")
    
    return payload


def get_current_user_id(current_user: Dict[str, Any] = Depends(get_current_user)) -> int:
    user_id = current_user.get("sub")
    
    if user_id is None:
        raise UnauthorizedException("Invalid token payload")
    
    try:
        return int(user_id)
    except ValueError:
        raise UnauthorizedException("Invalid user ID in token")


def get_current_user_email(current_user: Dict[str, Any] = Depends(get_current_user)) -> str:
    email = current_user.get("email")
    
    if email is None:
        raise UnauthorizedException("Invalid token payload")
    
    return email


def require_role(required_role: str):
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_role = current_user.get("role")
        
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}"
            )
        
        return current_user
    
    return role_checker


def optional_authentication(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict[str, Any]]:
    if credentials is None:
        return None
    
    token = credentials.credentials
    payload = JWTHandler.get_token_payload(token)
    
    return payload
