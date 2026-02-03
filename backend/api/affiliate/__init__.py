"""
Affiliate API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user, TokenData, UserRole
from schemas.models import (
    AffiliateLinkCreate, AffiliateLinkUpdate, AffiliateLinkResponse
)
from services.affiliate_service import AffiliateService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/affiliate", tags=["Affiliate"])


@router.post("/links", response_model=AffiliateLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_affiliate_link(
    link_data: AffiliateLinkCreate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new affiliate link (Admin/Affiliate Manager only).
    
    Args:
        link_data: Affiliate link data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Created affiliate link
    
    Raises:
        HTTPException: If user lacks permission
    """
    # Check authorization
    allowed_roles = [UserRole.SUPER_ADMIN, UserRole.AFFILIATE_MANAGER]
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and affiliate managers can create links"
        )
    
    try:
        link = AffiliateService.create_affiliate_link(db, link_data)
        return link
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating affiliate link: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create affiliate link"
        )


@router.get("/links/{link_id}", response_model=AffiliateLinkResponse)
async def get_affiliate_link(
    link_id: int,
    db: Session = Depends(get_db)
):
    """
    Get affiliate link by ID.
    
    Args:
        link_id: Affiliate link ID
        db: Database session
    
    Returns:
        Affiliate link details
    
    Raises:
        HTTPException: If link not found
    """
    link = AffiliateService.get_affiliate_link_by_id(db, link_id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Affiliate link {link_id} not found"
        )
    return link


@router.get("/product/{product_id}", response_model=list[AffiliateLinkResponse])
async def get_product_affiliate_links(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all affiliate links for a product.
    
    Args:
        product_id: Product ID
        db: Database session
    
    Returns:
        List of affiliate links for product
    """
    links = AffiliateService.get_affiliate_links_for_product(db, product_id)
    return links


@router.get("/platform/{platform}", response_model=list[AffiliateLinkResponse])
async def get_platform_links(
    platform: str,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get all affiliate links for a platform.
    
    Args:
        platform: Platform name (amazon, myntra, meesho, ajio, flipkart)
        limit: Maximum results
        db: Database session
    
    Returns:
        List of links for the platform
    """
    links = AffiliateService.get_links_by_platform(db, platform)
    return links[:limit]


@router.put("/links/{link_id}", response_model=AffiliateLinkResponse)
async def update_affiliate_link(
    link_id: int,
    link_data: AffiliateLinkUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an affiliate link (Admin/Affiliate Manager only).
    
    Args:
        link_id: Affiliate link ID
        link_data: Updated link data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Updated affiliate link
    
    Raises:
        HTTPException: If user lacks permission or link not found
    """
    # Check authorization
    allowed_roles = [UserRole.SUPER_ADMIN, UserRole.AFFILIATE_MANAGER]
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and affiliate managers can update links"
        )
    
    try:
        link = AffiliateService.update_affiliate_link(db, link_id, link_data)
        return link
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_affiliate_link(
    link_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an affiliate link (Admin only).
    
    Args:
        link_id: Affiliate link ID
        current_user: Current authenticated user
        db: Database session
    
    Raises:
        HTTPException: If user lacks permission or link not found
    """
    # Check authorization
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete affiliate links"
        )
    
    try:
        AffiliateService.delete_affiliate_link(db, link_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/platforms/", response_model=list[str])
async def get_all_platforms(db: Session = Depends(get_db)):
    """
    Get all active affiliate platforms.
    
    Args:
        db: Database session
    
    Returns:
        List of platform names
    """
    platforms = AffiliateService.get_all_platforms(db)
    return platforms or ["amazon", "myntra", "meesho", "ajio", "flipkart"]


@router.post("/bulk-create", response_model=list[AffiliateLinkResponse])
async def bulk_create_links(
    links_data: list[AffiliateLinkCreate],
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create multiple affiliate links at once.
    
    Args:
        links_data: List of affiliate link data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        List of created links
    
    Raises:
        HTTPException: If user lacks permission
    """
    # Check authorization
    allowed_roles = [UserRole.SUPER_ADMIN, UserRole.AFFILIATE_MANAGER]
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and affiliate managers can create links"
        )
    
    try:
        links = AffiliateService.bulk_create_affiliate_links(db, links_data)
        return links
    except Exception as e:
        logger.error(f"Error in bulk create: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create some affiliate links"
        )
