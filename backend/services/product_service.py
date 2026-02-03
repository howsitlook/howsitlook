"""
Product management service.
"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from schemas.base import Product
from schemas.models import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)


class ProductService:
    """Service for product management."""
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        """
        Create a new product.
        
        Args:
            db: Database session
            product_data: Product creation data
        
        Returns:
            Created Product object
        """
        product = Product(
            name=product_data.name,
            description=product_data.description,
            brand=product_data.brand,
            category=product_data.category,
            subcategory=product_data.subcategory,
            price=product_data.price,
            currency=product_data.currency,
            image_url=product_data.image_url,
            mask_url=product_data.mask_url,
            tags=product_data.tags,
            fabric_type=product_data.fabric_type,
            color=product_data.color,
            pattern=product_data.pattern,
            size_guide=product_data.size_guide
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        logger.info(f"Product created: {product.id} - {product.name}")
        return product
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
        """
        Get product by ID.
        
        Args:
            db: Database session
            product_id: Product ID
        
        Returns:
            Product object or None
        """
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_all_products(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        is_active: bool = True
    ) -> tuple[int, List[Product]]:
        """
        Get paginated products with optional filters.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum records to return
            category: Filter by category
            brand: Filter by brand
            search: Search in name and description
            min_price: Minimum price filter
            max_price: Maximum price filter
            is_active: Filter by active status
        
        Returns:
            Tuple of (total_count, products_list)
        """
        query = db.query(Product).filter(Product.is_active == is_active)
        
        if category:
            query = query.filter(Product.category == category)
        
        if brand:
            query = query.filter(Product.brand == brand)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_pattern),
                    Product.description.ilike(search_pattern)
                )
            )
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        return total, products
    
    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate
    ) -> Optional[Product]:
        """
        Update a product.
        
        Args:
            db: Database session
            product_id: Product ID
            product_data: Updated product data
        
        Returns:
            Updated Product object
        
        Raises:
            ValueError: If product not found
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        # Update fields if provided
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        
        logger.info(f"Product updated: {product_id}")
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """
        Delete a product (soft delete by marking inactive).
        
        Args:
            db: Database session
            product_id: Product ID
        
        Returns:
            True if successful
        
        Raises:
            ValueError: If product not found
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        product.is_active = False
        db.commit()
        
        logger.info(f"Product deleted: {product_id}")
        return True
    
    @staticmethod
    def get_products_by_category(
        db: Session,
        category: str,
        limit: int = 50
    ) -> List[Product]:
        """
        Get products by category.
        
        Args:
            db: Database session
            category: Product category
            limit: Maximum records
        
        Returns:
            List of products
        """
        return db.query(Product).filter(
            and_(
                Product.category == category,
                Product.is_active == True
            )
        ).limit(limit).all()
    
    @staticmethod
    def search_products(
        db: Session,
        query_text: str,
        limit: int = 50
    ) -> List[Product]:
        """
        Search products by name, brand, or tags.
        
        Args:
            db: Database session
            query_text: Search query
            limit: Maximum records
        
        Returns:
            List of matching products
        """
        search_pattern = f"%{query_text}%"
        return db.query(Product).filter(
            and_(
                or_(
                    Product.name.ilike(search_pattern),
                    Product.brand.ilike(search_pattern),
                    Product.description.ilike(search_pattern)
                ),
                Product.is_active == True
            )
        ).limit(limit).all()
