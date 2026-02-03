"""
AI Outfit Recommendation Engine using embeddings and ML.
Recommends outfits based on CLIP embeddings, color matching, and fashion rules.
"""
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from schemas.base import Product, Recommendation, User
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Recommendation engine using CLIP embeddings and fashion rules."""
    
    def __init__(self, top_k: int = 10):
        """
        Initialize recommendation engine.
        
        Args:
            top_k: Number of recommendations to return
        """
        self.top_k = top_k
        self.clip_model = None
        self.product_embeddings_cache = {}
        
        logger.info(f"Initializing RecommendationEngine with top_k={top_k}")
    
    def _load_clip_model(self):
        """
        Load CLIP model for embeddings (stub for production).
        Production: Use actual CLIP or other vision-language model.
        """
        try:
            # Production implementation:
            # import clip
            # self.clip_model = clip.load("ViT-B/32", device="cpu")
            
            logger.info("CLIP model loaded for embeddings")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            raise
    
    def get_product_embedding(self, product: Product) -> np.ndarray:
        """
        Get or compute CLIP embedding for product.
        
        Args:
            product: Product object
        
        Returns:
            Product embedding vector
        """
        try:
            if self.clip_model is None:
                self._load_clip_model()
            
            # Check cache
            if product.id in self.product_embeddings_cache:
                return self.product_embeddings_cache[product.id]
            
            # Stub: Generate random embedding (production uses actual CLIP)
            # In production:
            # - Use product image: product.image_url
            # - Use product text: name, description, tags
            # - Compute embedding via CLIP
            
            embedding = np.random.randn(512).astype(np.float32)
            embedding = embedding / np.linalg.norm(embedding)  # Normalize
            
            # Cache it
            self.product_embeddings_cache[product.id] = embedding
            
            return embedding
        
        except Exception as e:
            logger.error(f"Error getting embedding for product {product.id}: {e}")
            raise
    
    def compute_similarity(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray
    ) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
        
        Returns:
            Cosine similarity score (0-1)
        """
        try:
            # Normalize
            e1 = embedding1 / (np.linalg.norm(embedding1) + 1e-8)
            e2 = embedding2 / (np.linalg.norm(embedding2) + 1e-8)
            
            similarity = float(np.dot(e1, e2))
            return max(0.0, min(1.0, similarity))
        
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
    
    def apply_fashion_rules(
        self,
        base_product: Product,
        candidate: Product,
        user: Optional[User] = None
    ) -> float:
        """
        Apply fashion rules to adjust recommendation score.
        Rules:
        - Color harmony
        - Category compatibility
        - Price range match (optional)
        - Body type suitability
        
        Args:
            base_product: Reference product
            candidate: Candidate product
            user: User object (for body type, skin tone)
        
        Returns:
            Adjustment factor (0-2, where 1.0 = no adjustment)
        """
        try:
            adjustment = 1.0
            
            # Color harmony rule
            if base_product.color and candidate.color:
                colors_match = self._check_color_harmony(
                    base_product.color,
                    candidate.color
                )
                if colors_match:
                    adjustment *= 1.3
                else:
                    adjustment *= 0.8
            
            # Category compatibility
            if base_product.category == candidate.category:
                adjustment *= 0.7  # Reduce score for same category
            
            # Price range match (similar price = good pairing)
            price_ratio = min(base_product.price, candidate.price) / max(base_product.price, candidate.price)
            if 0.5 <= price_ratio <= 2.0:
                adjustment *= 1.1
            
            # Body type suitability
            if user and user.body_type:
                if self._is_suitable_for_body_type(candidate, user.body_type):
                    adjustment *= 1.2
            
            return adjustment
        
        except Exception as e:
            logger.error(f"Error applying fashion rules: {e}")
            return 1.0
    
    def _check_color_harmony(self, color1: str, color2: str) -> bool:
        """
        Check if two colors are harmonious.
        Simplified rule-based approach. Production: Use color theory.
        
        Args:
            color1: First color
            color2: Second color
        
        Returns:
            True if colors harmonize
        """
        # Simplified color harmony (in production, use actual color theory)
        complementary_pairs = [
            ("red", "blue"), ("blue", "red"),
            ("yellow", "purple"), ("purple", "yellow"),
            ("green", "red"), ("red", "green"),
            ("orange", "blue"), ("blue", "orange"),
        ]
        
        color1_lower = color1.lower()
        color2_lower = color2.lower()
        
        # Check exact matches
        if (color1_lower, color2_lower) in complementary_pairs:
            return True
        
        # Neutral colors pair well with everything
        neutrals = ["black", "white", "gray", "beige", "navy"]
        if color1_lower in neutrals or color2_lower in neutrals:
            return True
        
        # Similar colors (from same family)
        color_families = [
            ["red", "pink", "burgundy"],
            ["blue", "navy", "teal"],
            ["green", "olive", "khaki"],
            ["yellow", "gold", "orange"],
        ]
        
        for family in color_families:
            if color1_lower in family and color2_lower in family:
                return True
        
        return False
    
    def _is_suitable_for_body_type(self, product: Product, body_type: str) -> bool:
        """
        Check if product is suitable for body type.
        Stub: In production, use ML model trained on body-type data.
        
        Args:
            product: Product object
            body_type: Body type (pear, apple, hourglass, etc.)
        
        Returns:
            True if suitable
        """
        # Simplified rules
        if body_type == "pear":
            # Avoid patterns that add width at bottom
            return product.category not in ["bottoms", "skirts"]
        elif body_type == "apple":
            # Good: Flows from waist, draws focus up
            return product.category == "tops" or product.category == "dresses"
        elif body_type == "hourglass":
            # Fitted styles
            return True
        elif body_type == "rectangle":
            # Add curves, belted styles
            return product.category != "blazers"
        
        return True
    
    def knn_similarity_search(
        self,
        db: Session,
        base_product: Product,
        all_products: List[Product],
        k: int = 10,
        user: Optional[User] = None
    ) -> List[Tuple[Product, float]]:
        """
        Find k-nearest products to base product using embeddings.
        
        Args:
            db: Database session
            base_product: Reference product
            all_products: Candidate products
            k: Number of recommendations
            user: Optional user for context
        
        Returns:
            List of (product, similarity_score) tuples
        """
        try:
            base_embedding = self.get_product_embedding(base_product)
            
            similarities = []
            for product in all_products:
                if product.id == base_product.id:
                    continue  # Skip the base product itself
                
                # Get embedding
                embedding = self.get_product_embedding(product)
                
                # Compute similarity
                similarity = self.compute_similarity(base_embedding, embedding)
                
                # Apply fashion rules
                adjustment = self.apply_fashion_rules(base_product, product, user)
                final_score = similarity * adjustment
                
                similarities.append((product, final_score))
            
            # Sort by score and return top k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:k]
        
        except Exception as e:
            logger.error(f"Error in KNN search: {e}")
            return []
    
    async def recommend_outfits(
        self,
        db: Session,
        user_id: int,
        base_product_id: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate outfit recommendations for user.
        
        Args:
            db: Database session
            user_id: User ID
            base_product_id: Optional product to base recommendations on
            filters: Optional filters (category, price range, etc.)
        
        Returns:
            Dictionary with recommendations
        """
        try:
            logger.info(f"Generating recommendations for user {user_id}")
            
            # Get user
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Get all active products
            all_products = db.query(Product).filter(Product.is_active == True).all()
            
            if not all_products:
                logger.warning("No active products found")
                return {
                    "user_id": user_id,
                    "recommendations": [],
                    "reason": "No products available",
                    "count": 0
                }
            
            # If no base product specified, recommend popular items
            if base_product_id is None:
                # Stub: Return random popular products
                recommendations = all_products[:self.top_k]
                reason = "Popular items recommendation"
            else:
                # Get base product
                base_product = db.query(Product).filter(
                    Product.id == base_product_id
                ).first()
                
                if not base_product:
                    raise ValueError(f"Product {base_product_id} not found")
                
                # Find similar products
                similar_products = self.knn_similarity_search(
                    db,
                    base_product,
                    all_products,
                    k=self.top_k,
                    user=user
                )
                
                recommendations = [
                    {
                        "product": p,
                        "score": score
                    }
                    for p, score in similar_products
                ]
                
                reason = f"Similar to {base_product.name}"
            
            # Build response
            recommended_items = []
            for item in recommendations:
                if isinstance(item, dict):
                    product = item["product"]
                    score = item["score"]
                else:
                    product = item
                    score = 0.85
                
                recommended_items.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "brand": product.brand,
                    "image_url": product.image_url,
                    "price": product.price,
                    "category": product.category,
                    "similarity_score": float(score),
                    "reason": reason
                })
            
            # Save recommendation to database
            rec = Recommendation(
                user_id=user_id,
                recommended_products=[item["product_id"] for item in recommended_items],
                reason=reason,
                base_product_id=base_product_id,
                similarity_scores=[item["similarity_score"] for item in recommended_items]
            )
            
            db.add(rec)
            db.commit()
            db.refresh(rec)
            
            logger.info(f"Generated {len(recommended_items)} recommendations for user {user_id}")
            
            return {
                "recommendation_id": rec.id,
                "user_id": user_id,
                "recommendations": recommended_items,
                "reason": reason,
                "count": len(recommended_items),
                "created_at": rec.created_at
            }
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            raise
    
    def clear_embedding_cache(self):
        """Clear product embedding cache."""
        self.product_embeddings_cache.clear()
        logger.info("Embedding cache cleared")
