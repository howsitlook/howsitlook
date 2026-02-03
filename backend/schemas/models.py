"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any


# ==================== AUTH SCHEMAS ====================

class UserRegister(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=128)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Schema for token refresh."""
    refresh_token: str


class UserResponse(BaseModel):
    """Schema for user profile response."""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str]
    body_type: Optional[str]
    skin_tone: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for user profile update."""
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    body_type: Optional[str] = None
    skin_tone: Optional[str] = None


# ==================== PRODUCT SCHEMAS ====================

class ProductCreate(BaseModel):
    """Schema for creating a product."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    brand: str = Field(..., min_length=1, max_length=128)
    category: str = Field(..., min_length=1, max_length=128)
    subcategory: Optional[str] = None
    price: float = Field(..., gt=0)
    currency: str = "INR"
    image_url: str
    mask_url: Optional[str] = None
    tags: Optional[List[str]] = None
    fabric_type: Optional[str] = None
    color: Optional[str] = None
    pattern: Optional[str] = None
    size_guide: Optional[Dict[str, Any]] = None


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    mask_url: Optional[str] = None
    tags: Optional[List[str]] = None
    fabric_type: Optional[str] = None
    color: Optional[str] = None
    pattern: Optional[str] = None
    size_guide: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    """Schema for product response."""
    id: int
    name: str
    description: Optional[str]
    brand: str
    category: str
    subcategory: Optional[str]
    price: float
    currency: str
    image_url: str
    mask_url: Optional[str]
    tags: Optional[List[str]]
    fabric_type: Optional[str]
    color: Optional[str]
    pattern: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for product list with pagination."""
    total: int
    skip: int
    limit: int
    items: List[ProductResponse]


# ==================== AFFILIATE SCHEMAS ====================

class AffiliateLinkCreate(BaseModel):
    """Schema for creating affiliate link."""
    product_id: int
    platform: str = Field(..., min_length=1, max_length=50)
    affiliate_url: str
    product_sku: Optional[str] = None
    commission_rate: Optional[float] = 0.0


class AffiliateLinkUpdate(BaseModel):
    """Schema for updating affiliate link."""
    affiliate_url: Optional[str] = None
    commission_rate: Optional[float] = None
    is_active: Optional[bool] = None


class AffiliateLinkResponse(BaseModel):
    """Schema for affiliate link response."""
    id: int
    product_id: int
    platform: str
    affiliate_url: str
    product_sku: Optional[str]
    commission_rate: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== TRY-ON SCHEMAS ====================

class TryOnRequest(BaseModel):
    """Schema for virtual try-on request."""
    user_id: int
    product_id: int
    avatar_image: Optional[str] = None  # Base64 or path
    target_pose: Optional[Dict[str, Any]] = None
    body_shape: Optional[str] = None


class TryOnResponse(BaseModel):
    """Schema for try-on result."""
    id: int
    user_id: int
    product_id: int
    result_image_url: str
    confidence_score: float
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== POSE TRANSFER SCHEMAS ====================

class PoseTransferRequest(BaseModel):
    """Schema for pose transfer request."""
    user_id: int
    source_image: Optional[str] = None  # Base64 or path
    target_pose: Dict[str, Any]  # Pose keypoints


class PoseTransferResponse(BaseModel):
    """Schema for pose transfer result."""
    id: int
    user_id: int
    result_image_url: str
    confidence_score: float
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== RECOMMENDATION SCHEMAS ====================

class RecommendationRequest(BaseModel):
    """Schema for recommendation request."""
    user_id: int
    base_product_id: Optional[int] = None  # Recommend items matching this
    top_k: int = 10
    filters: Optional[Dict[str, Any]] = None  # Category, color, price range, etc.


class RecommendedItem(BaseModel):
    """Schema for a recommended item."""
    product_id: int
    product_name: str
    brand: str
    image_url: str
    similarity_score: float
    price: float
    reason: Optional[str]


class RecommendationResponse(BaseModel):
    """Schema for recommendation response."""
    id: int
    user_id: int
    recommendations: List[RecommendedItem]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== ADMIN SCHEMAS ====================

class AdminUserResponse(BaseModel):
    """Schema for admin viewing user."""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AdminUserListResponse(BaseModel):
    """Schema for admin user list."""
    total: int
    skip: int
    limit: int
    items: List[AdminUserResponse]


class AdminStatsResponse(BaseModel):
    """Schema for admin dashboard stats."""
    total_users: int
    total_products: int
    total_tryon_results: int
    active_users_today: int
    affiliate_platforms: List[str]
    top_products: List[Dict[str, Any]]
