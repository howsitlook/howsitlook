"""
Authentication service with JWT and user management.
"""
import logging
from sqlalchemy.orm import Session
from schemas.base import User
from schemas.models import UserRegister, UserLogin, TokenResponse
from core.security import (
    hash_password, verify_password, create_access_token,
    create_refresh_token, verify_token, UserRole
)

logger = logging.getLogger(__name__)


class AuthService:
    """Service for user authentication and JWT management."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_data: User registration data
        
        Returns:
            Created User object
        
        Raises:
            ValueError: If email or username already exists
        """
        # Check if user already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise ValueError(f"Email {user_data.email} already registered")
        
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise ValueError(f"Username {user_data.username} already taken")
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=UserRole.USER,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"New user registered: {new_user.email}")
        return new_user
    
    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> TokenResponse:
        """
        Authenticate user and return tokens.
        
        Args:
            db: Database session
            login_data: Login credentials
        
        Returns:
            TokenResponse with access and refresh tokens
        
        Raises:
            ValueError: If credentials are invalid
        """
        # Find user by email
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise ValueError("Invalid credentials")
        
        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("User account is inactive")
        
        # Create tokens
        access_token = create_access_token(
            subject=str(user.id),
            role=user.role
        )
        refresh_token = create_refresh_token(
            subject=str(user.id),
            role=user.role
        )
        
        logger.info(f"User logged in: {user.email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800  # 30 minutes
        )
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> TokenResponse:
        """
        Create new access token from refresh token.
        
        Args:
            refresh_token: Valid refresh token
        
        Returns:
            TokenResponse with new access token
        
        Raises:
            ValueError: If refresh token is invalid
        """
        token_data = verify_token(refresh_token)
        
        # Create new access token
        new_access_token = create_access_token(
            subject=token_data.subject,
            role=token_data.role
        )
        
        # Create new refresh token
        new_refresh_token = create_refresh_token(
            subject=token_data.subject,
            role=token_data.role
        )
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=1800
        )
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            User object
        
        Raises:
            ValueError: If user not found
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """
        Get user by email.
        
        Args:
            db: Database session
            email: User email
        
        Returns:
            User object
        
        Raises:
            ValueError: If user not found
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError(f"User with email {email} not found")
        return user
    
    @staticmethod
    def update_user_role(db: Session, user_id: int, new_role: str) -> User:
        """
        Update user role (admin only).
        
        Args:
            db: Database session
            user_id: User ID
            new_role: New role string
        
        Returns:
            Updated User object
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.role = new_role
        db.commit()
        db.refresh(user)
        
        logger.info(f"User {user.email} role updated to {new_role}")
        return user
    
    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> User:
        """
        Deactivate user account.
        
        Args:
            db: Database session
            user_id: User ID
        
        Returns:
            Updated User object
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.is_active = False
        db.commit()
        db.refresh(user)
        
        logger.info(f"User {user.email} deactivated")
        return user
