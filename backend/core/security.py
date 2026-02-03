"""
Security utilities for JWT authentication and role-based access control.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from core.config import get_settings
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


# Simple credentials model to replace HTTPAuthCredentials
class HTTPAuthCredentials:
    """HTTP Bearer credentials model."""
    def __init__(self, scheme: str, credentials: str):
        self.scheme = scheme
        self.credentials = credentials


# Role enumeration
class UserRole:
    """User roles for RBAC."""
    SUPER_ADMIN = "super_admin"
    AFFILIATE_MANAGER = "affiliate_manager"
    CONTENT_MANAGER = "content_manager"
    AI_MANAGER = "ai_manager"
    VIEWER = "viewer"
    USER = "user"


class TokenData:
    """Data model for decoded JWT tokens."""
    def __init__(self, sub: str, role: str, exp: datetime):
        self.subject = sub
        self.role = role
        self.expires = exp


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    role: str = UserRole.USER,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: User identifier (typically user_id or email)
        role: User role for RBAC
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT token
    """
    settings = get_settings()
    
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(subject: str, role: str = UserRole.USER) -> str:
    """
    Create a JWT refresh token with longer expiration.
    
    Args:
        subject: User identifier
        role: User role
    
    Returns:
        Encoded refresh token
    """
    settings = get_settings()
    expires_delta = timedelta(days=settings.refresh_token_expire_days)
    
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": subject,
        "role": role,
        "type": "refresh",
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token to verify
    
    Returns:
        TokenData with decoded information
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        subject: str = payload.get("sub")
        role: str = payload.get("role", UserRole.USER)
        exp: datetime = datetime.fromtimestamp(
            payload.get("exp"),
            tz=timezone.utc
        )
        
        if subject is None:
            raise credentials_exception
        
        return TokenData(sub=subject, role=role, exp=exp)
    
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise credentials_exception


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> TokenData:
    """
    Dependency to get current authenticated user from Bearer token.
    
    Args:
        credentials: HTTP Bearer credentials
    
    Returns:
        TokenData of authenticated user
    
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    return verify_token(token)


async def get_current_user_with_role(
    required_roles: List[str]
) -> callable:
    """
    Create a dependency that checks user has one of required roles.
    
    Args:
        required_roles: List of allowed roles
    
    Returns:
        Dependency function for FastAPI
    """
    async def role_checker(user: TokenData = Depends(get_current_user)) -> TokenData:
        if user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.role}' does not have access to this resource"
            )
        return user
    
    return role_checker
