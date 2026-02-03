"""
Product API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user, TokenData, get_current_user_with_role, UserRole
from schemas.models import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
)
from services.product_service import ProductService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new product (Admin/Content Manager only).
    
    Args:
        product_data: Product creation data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Created product
    
    Raises:
        HTTPException: If user lacks permission
    """
    # Check authorization
    allowed_roles = [UserRole.SUPER_ADMIN, UserRole.CONTENT_MANAGER]
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and content managers can create products"
        )
    
    try:
        product = ProductService.create_product(db, product_data)
        return product
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )


@router.get("/", response_model=ProductListResponse)
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: str = Query(None),
    brand: str = Query(None),
    search: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all products with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum records to return
        category: Filter by category
        brand: Filter by brand
        search: Search in name/description
        min_price: Minimum price
        max_price: Maximum price
        db: Database session
    
    Returns:
        List of products with pagination info
    """
    total, products = ProductService.get_all_products(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        brand=brand,
        search=search,
        min_price=min_price,
        max_price=max_price
    )
    
    return ProductListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=products
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get product by ID.
    
    Args:
        product_id: Product ID
        db: Database session
    
    Returns:
        Product details
    
    Raises:
        HTTPException: If product not found
    """
    product = ProductService.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a product (Admin/Content Manager only).
    
    Args:
        product_id: Product ID
        product_data: Updated product data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Updated product
    
    Raises:
        HTTPException: If user lacks permission or product not found
    """
    # Check authorization
    allowed_roles = [UserRole.SUPER_ADMIN, UserRole.CONTENT_MANAGER]
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and content managers can update products"
        )
    
    try:
        product = ProductService.update_product(db, product_id, product_data)
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product"
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a product (Admin only).
    
    Args:
        product_id: Product ID
        current_user: Current authenticated user
        db: Database session
    
    Raises:
        HTTPException: If user lacks permission or product not found
    """
    # Check authorization
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete products"
        )
    
    try:
        ProductService.delete_product(db, product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/category/{category}", response_model=list[ProductResponse])
async def get_products_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all products in a category.
    
    Args:
        category: Product category
        limit: Maximum records
        db: Database session
    
    Returns:
        List of products in category
    """
    products = ProductService.get_products_by_category(db, category, limit)
    return products


@router.get("/search/{query_text}", response_model=list[ProductResponse])
async def search_products(
    query_text: str,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search products.
    
    Args:
        query_text: Search query
        limit: Maximum results
        db: Database session
    
    Returns:
        List of matching products
    """
    products = ProductService.search_products(db, query_text, limit)
    return products
