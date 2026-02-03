"""
Authentication API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user, UserRole, TokenData, get_current_user_with_role
from schemas.models import (
    UserRegister, UserLogin, TokenResponse, RefreshTokenRequest,
    UserResponse, UserUpdate
)
from services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
    
    Returns:
        Created user profile
    
    Raises:
        HTTPException: If email or username already exists
    """
    try:
        user = AuthService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT tokens.
    
    Args:
        login_data: Login credentials
        db: Database session
    
    Returns:
        TokenResponse with access and refresh tokens
    
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        return AuthService.login_user(db, login_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_req: RefreshTokenRequest):
    """
    Refresh access token using refresh token.
    
    Args:
        refresh_req: Refresh token request
    
    Returns:
        TokenResponse with new access and refresh tokens
    
    Raises:
        HTTPException: If refresh token is invalid
    """
    try:
        return AuthService.refresh_access_token(refresh_req.refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user profile.
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Current user profile
    """
    try:
        user = AuthService.get_user_by_id(db, int(current_user.subject))
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile.
    
    Args:
        user_update: Updated user data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Updated user profile
    """
    try:
        user = AuthService.get_user_by_id(db, int(current_user.subject))
        
        # Update fields if provided
        if user_update.full_name is not None:
            user.full_name = user_update.full_name
        if user_update.avatar_url is not None:
            user.avatar_url = user_update.avatar_url
        if user_update.body_type is not None:
            user.body_type = user_update.body_type
        if user_update.skin_tone is not None:
            user.skin_tone = user_update.skin_tone
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"User {user.email} profile updated")
        return user
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/logout")
async def logout(current_user: TokenData = Depends(get_current_user)):
    """
    Logout user. (Token-based, so just acknowledge logout)
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Logout confirmation
    """
    logger.info(f"User {current_user.subject} logged out")
    return {"message": "Successfully logged out"}
