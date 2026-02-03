"""
Virtual Try-On API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user, TokenData
from schemas.models import TryOnRequest, TryOnResponse
from services.vton_service import VirtualTryOnService
from schemas.base import TryOnResult, Product
import logging
import tempfile
import os
from core.config import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tryon", tags=["Virtual Try-On"])
settings = get_settings()


@router.post("/run", response_model=TryOnResponse)
async def run_virtual_tryon(
    product_id: int = Form(...),
    avatar_image: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Run virtual try-on for a product.
    
    Args:
        product_id: Product ID to try on
        avatar_image: User's photo/avatar
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Try-on result with image
    
    Raises:
        HTTPException: If product not found or try-on fails
    """
    try:
        user_id = int(current_user.subject)
        
        # Check product exists
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found"
            )
        
        # Save uploaded image temporarily
        with tempfile.TemporaryDirectory() as temp_dir:
            avatar_path = os.path.join(temp_dir, avatar_image.filename)
            with open(avatar_path, "wb") as f:
                content = await avatar_image.read()
                f.write(content)
            
            # Load images using service
            vton_service = VirtualTryOnService(
                model_type=settings.vton_model_name,
                device=settings.model_device
            )
            
            avatar_img = vton_service.load_image_from_file(avatar_path)
            garment_img = vton_service.load_image_from_file(product.image_url)
            
            # Run try-on
            result = await vton_service.run_tryon(
                avatar_image=avatar_img,
                garment_image=garment_img,
                body_shape=None,  # Could get from user profile
                output_path=settings.output_dir
            )
        
        # Save result to database
        tryon_result = TryOnResult(
            user_id=user_id,
            product_id=product_id,
            avatar_image_path=avatar_path if os.path.exists(avatar_path) else None,
            garment_image_path=product.image_url,
            result_image_path=result["result_filepath"],
            confidence_score=result["confidence_score"],
            metadata=result["metadata"]
        )
        
        db.add(tryon_result)
        db.commit()
        db.refresh(tryon_result)
        
        logger.info(f"Try-on completed for user {user_id}, product {product_id}")
        
        return TryOnResponse(
            id=tryon_result.id,
            user_id=user_id,
            product_id=product_id,
            result_image_url=result["result_base64"],
            confidence_score=result["confidence_score"],
            metadata=result["metadata"],
            created_at=tryon_result.created_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Virtual try-on failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Virtual try-on failed"
        )


@router.get("/results/{tryon_id}", response_model=TryOnResponse)
async def get_tryon_result(
    tryon_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a previous try-on result.
    
    Args:
        tryon_id: Try-on result ID
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Try-on result details
    
    Raises:
        HTTPException: If result not found or unauthorized
    """
    try:
        result = db.query(TryOnResult).filter(TryOnResult.id == tryon_id).first()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Try-on result {tryon_id} not found"
            )
        
        # Check authorization
        if result.user_id != int(current_user.subject):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own try-on results"
            )
        
        return TryOnResponse(
            id=result.id,
            user_id=result.user_id,
            product_id=result.product_id,
            result_image_url=result.result_image_path,
            confidence_score=result.confidence_score,
            metadata=result.metadata,
            created_at=result.created_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving try-on result: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve try-on result"
        )


@router.get("/my-results")
async def get_user_tryon_results(
    skip: int = 0,
    limit: int = 20,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all try-on results for current user.
    
    Args:
        skip: Offset
        limit: Maximum results
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        List of try-on results
    """
    try:
        user_id = int(current_user.subject)
        
        total = db.query(TryOnResult).filter(
            TryOnResult.user_id == user_id
        ).count()
        
        results = db.query(TryOnResult).filter(
            TryOnResult.user_id == user_id
        ).offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": [
                {
                    "id": r.id,
                    "product_id": r.product_id,
                    "result_image_url": r.result_image_path,
                    "confidence_score": r.confidence_score,
                    "created_at": r.created_at
                }
                for r in results
            ]
        }
    
    except Exception as e:
        logger.error(f"Error retrieving user try-on results: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve try-on results"
        )
