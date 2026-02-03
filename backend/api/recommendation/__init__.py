"""
AI Recommendation API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import get_current_user, TokenData
from schemas.models import RecommendationResponse
from services.reco_engine import RecommendationEngine
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendation", tags=["Recommendations"])

# Initialize recommendation engine
reco_engine = RecommendationEngine(top_k=10)


@router.post("/outfits", response_model=RecommendationResponse)
async def get_outfit_recommendations(
    base_product_id: Optional[int] = Query(None),
    top_k: int = Query(10, ge=1, le=50),
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get outfit recommendations for user.
    
    Args:
        base_product_id: Optional product to base recommendations on
        top_k: Number of recommendations (default 10)
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Outfit recommendations
    
    Raises:
        HTTPException: If recommendations generation fails
    """
    try:
        user_id = int(current_user.subject)
        
        # Generate recommendations
        result = await reco_engine.recommend_outfits(
            db=db,
            user_id=user_id,
            base_product_id=base_product_id
        )
        
        # Convert to response model
        return RecommendationResponse(
            id=result.get("recommendation_id", 0),
            user_id=user_id,
            recommendations=[
                {
                    "product_id": item["product_id"],
                    "product_name": item["product_name"],
                    "brand": item["brand"],
                    "image_url": item["image_url"],
                    "similarity_score": item["similarity_score"],
                    "price": item["price"],
                    "reason": item["reason"]
                }
                for item in result["recommendations"]
            ],
            created_at=result.get("created_at")
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )


@router.get("/similar/{product_id}")
async def get_similar_products(
    product_id: int,
    top_k: int = Query(10, ge=1, le=50),
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get products similar to a specific product.
    
    Args:
        product_id: Product ID
        top_k: Number of similar products
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Similar products
    """
    try:
        user_id = int(current_user.subject)
        
        # Generate recommendations based on product
        result = await reco_engine.recommend_outfits(
            db=db,
            user_id=user_id,
            base_product_id=product_id
        )
        
        return {
            "base_product_id": product_id,
            "similar_products": result["recommendations"],
            "count": len(result["recommendations"])
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error finding similar products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to find similar products"
        )


@router.get("/trending")
async def get_trending_outfits(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get trending outfit combinations.
    
    Args:
        limit: Number of trending outfits
        db: Database session
    
    Returns:
        Trending outfit recommendations
    """
    try:
        # Stub: In production, would query most popular combinations
        from schemas.base import Product
        
        products = db.query(Product).filter(
            Product.is_active == True
        ).limit(limit).all()
        
        return {
            "trending_outfits": [
                {
                    "product_id": p.id,
                    "name": p.name,
                    "brand": p.brand,
                    "image_url": p.image_url,
                    "price": p.price,
                    "popularity_score": 0.85
                }
                for p in products
            ],
            "count": len(products)
        }
    
    except Exception as e:
        logger.error(f"Error retrieving trending outfits: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve trending outfits"
        )


@router.post("/personalized")
async def get_personalized_recommendations(
    filters: Optional[Dict[str, Any]] = None,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized recommendations based on user profile.
    
    Args:
        filters: Optional filters
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Personalized recommendations
    """
    try:
        user_id = int(current_user.subject)
        
        # Generate personalized recommendations
        result = await reco_engine.recommend_outfits(
            db=db,
            user_id=user_id,
            filters=filters
        )
        
        return {
            "user_id": user_id,
            "personalized_recommendations": result["recommendations"],
            "count": len(result["recommendations"]),
            "filters": filters or {}
        }
    
    except Exception as e:
        logger.error(f"Error generating personalized recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate personalized recommendations"
        )
