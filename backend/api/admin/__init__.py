"""
Admin Panel API routes.
Role-based access control for Super Admin, Affiliate Manager, etc.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import (
    get_current_user, TokenData, UserRole,
    get_current_user_with_role
)
from schemas.models import (
    AdminUserResponse, AdminUserListResponse, AdminStatsResponse,
    UserUpdate
)
from schemas.base import User, Product, TryOnResult, AffiliateLink, Recommendation
from services.auth_service import AuthService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin Panel"])


async def admin_only(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Dependency to ensure only super admin access."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    return current_user


@router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    current_user: TokenData = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics.
    
    Args:
        current_user: Current admin user
        db: Database session
    
    Returns:
        Admin dashboard statistics
    """
    try:
        total_users = db.query(User).count()
        total_products = db.query(Product).filter(Product.is_active == True).count()
        total_tryon = db.query(TryOnResult).count()
        
        # Active users in last 24 hours (stub)
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        active_today = db.query(User).filter(
            User.updated_at >= one_day_ago
        ).count()
        
        # Get all platforms
        platforms = db.query(AffiliateLink.platform).distinct().all()
        platform_list = [p[0] for p in platforms]
        
        # Top 5 products by try-on count (stub)
        top_products = db.query(
            Product.id, Product.name, Product.brand
        ).limit(5).all()
        
        return AdminStatsResponse(
            total_users=total_users,
            total_products=total_products,
            total_tryon_results=total_tryon,
            active_users_today=active_today,
            affiliate_platforms=platform_list or ["amazon", "myntra", "meesho", "ajio", "flipkart"],
            top_products=[
                {"id": p.id, "name": p.name, "brand": p.brand}
                for p in top_products
            ]
        )
    
    except Exception as e:
        logger.error(f"Error getting admin stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve statistics"
        )


@router.get("/users", response_model=AdminUserListResponse)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    role: str = Query(None),
    is_active: bool = Query(None),
    current_user: TokenData = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    List all users with optional filtering.
    
    Args:
        skip: Offset
        limit: Maximum results
        role: Filter by role
        is_active: Filter by active status
        current_user: Current admin user
        db: Database session
    
    Returns:
        List of users
    """
    try:
        query = db.query(User)
        
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        
        return AdminUserListResponse(
            total=total,
            skip=skip,
            limit=limit,
            items=[AdminUserResponse.from_orm(u) for u in users]
        )
    
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list users"
        )


@router.get("/users/{user_id}", response_model=AdminUserResponse)
async def get_user_details(
    user_id: int,
    current_user: TokenData = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Get detailed user information.
    
    Args:
        user_id: User ID
        current_user: Current admin user
        db: Database session
    
    Returns:
        User details
    """
    try:
        user = AuthService.get_user_by_id(db, user_id)
        return AdminUserResponse.from_orm(user)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    new_role: str,
    current_user: TokenData = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Update user role.
    
    Args:
        user_id: User ID
        new_role: New role (super_admin, affiliate_manager, content_manager, ai_manager, viewer, user)
        current_user: Current admin user
        db: Database session
    
    Returns:
        Updated user
    """
    valid_roles = [
        UserRole.SUPER_ADMIN,
        UserRole.AFFILIATE_MANAGER,
        UserRole.CONTENT_MANAGER,
        UserRole.AI_MANAGER,
        UserRole.VIEWER,
        UserRole.USER
    ]
    
    if new_role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        )
    
    try:
        user = AuthService.update_user_role(db, user_id, new_role)
        return {
            "user_id": user.id,
            "email": user.email,
            "new_role": user.role,
            "message": "User role updated successfully"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    current_user: TokenData = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Deactivate user account.
    
    Args:
        user_id: User ID
        current_user: Current admin user
        db: Database session
    
    Returns:
        Confirmation message
    """
    try:
        user = AuthService.deactivate_user(db, user_id)
        return {
            "user_id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "message": "User deactivated successfully"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: TokenData = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Activate user account.
    
    Args:
        user_id: User ID
        current_user: Current admin user
        db: Database session
    
    Returns:
        Confirmation message
    """
    try:
        user = AuthService.get_user_by_id(db, user_id)
        user.is_active = True
        db.commit()
        db.refresh(user)
        
        return {
            "user_id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "message": "User activated successfully"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/activity-log")
async def get_activity_log(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: TokenData = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Get activity log (try-ons, recommendations, etc).
    
    Args:
        skip: Offset
        limit: Maximum results
        current_user: Current admin user
        db: Database session
    
    Returns:
        Activity log
    """
    try:
        tryon_logs = db.query(TryOnResult).offset(skip).limit(limit).all()
        
        return {
            "activity_type": "try_on_results",
            "total": db.query(TryOnResult).count(),
            "logs": [
                {
                    "user_id": log.user_id,
                    "product_id": log.product_id,
                    "confidence": log.confidence_score,
                    "created_at": log.created_at
                }
                for log in tryon_logs
            ]
        }
    
    except Exception as e:
        logger.error(f"Error retrieving activity log: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve activity log"
        )


@router.get("/recommendation-metrics")
async def get_recommendation_metrics(
    current_user: TokenData = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Get recommendation engine metrics.
    
    Args:
        current_user: Current admin user
        db: Database session
    
    Returns:
        Recommendation metrics
    """
    try:
        total_recommendations = db.query(Recommendation).count()
        avg_recommendations_per_user = db.query(Recommendation).count() / max(db.query(User).count(), 1)
        
        return {
            "total_recommendations": total_recommendations,
            "avg_per_user": avg_recommendations_per_user,
            "active_users": db.query(User).filter(User.is_active == True).count(),
            "model_type": "CLIP-based with fashion rules",
            "status": "operational"
        }
    
    except Exception as e:
        logger.error(f"Error getting recommendation metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve recommendation metrics"
        )
