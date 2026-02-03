"""
SQLAlchemy Base and ORM models for the application.
"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from datetime import datetime
from typing import Optional

Base = declarative_base()


class User(Base):
    """User model for authentication and profile."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="user", nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String(512), nullable=True)
    body_type = Column(String(50), nullable=True)  # e.g., pear, apple, hourglass
    skin_tone = Column(String(50), nullable=True)  # for color matching
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class Product(Base):
    """Product/Clothing item model."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    brand = Column(String(128), nullable=False, index=True)
    category = Column(String(128), nullable=False, index=True)
    subcategory = Column(String(128), nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    image_url = Column(String(512), nullable=False)
    mask_url = Column(String(512), nullable=True)  # Segmentation mask
    tags = Column(JSON, nullable=True)  # e.g., ["casual", "summer", "cotton"]
    fabric_type = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)
    pattern = Column(String(50), nullable=True)
    size_guide = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, brand={self.brand})>"


class AffiliateLink(Base):
    """Affiliate link mappings for products."""
    __tablename__ = "affiliate_links"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    platform = Column(String(50), nullable=False, index=True)  # amazon, myntra, meesho, etc.
    affiliate_url = Column(String(512), nullable=False)
    product_sku = Column(String(128), nullable=True)
    commission_rate = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<AffiliateLink(product_id={self.product_id}, platform={self.platform})>"


class TryOnResult(Base):
    """Virtual try-on result storage."""
    __tablename__ = "tryon_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    avatar_image_path = Column(String(512), nullable=True)
    garment_image_path = Column(String(512), nullable=True)
    result_image_path = Column(String(512), nullable=False)
    pose_used = Column(JSON, nullable=True)  # Pose keypoints
    confidence_score = Column(Float, default=0.0)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<TryOnResult(user_id={self.user_id}, product_id={self.product_id})>"


class PoseTransferResult(Base):
    """Pose transfer result storage."""
    __tablename__ = "pose_transfer_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    source_image_path = Column(String(512), nullable=False)
    source_pose = Column(JSON, nullable=True)
    target_pose = Column(JSON, nullable=False)
    result_image_path = Column(String(512), nullable=False)
    confidence_score = Column(Float, default=0.0)
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PoseTransferResult(user_id={self.user_id})>"


class Recommendation(Base):
    """Outfit recommendation results."""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    recommended_products = Column(JSON, nullable=False)  # List of product IDs
    reason = Column(Text, nullable=True)
    base_product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    similarity_scores = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Recommendation(user_id={self.user_id}, products={len(self.recommended_products)})>"
