"""
Affiliate link management service.
"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.base import AffiliateLink, Product
from schemas.models import AffiliateLinkCreate, AffiliateLinkUpdate

logger = logging.getLogger(__name__)


class AffiliateService:
    """Service for affiliate link management."""
    
    @staticmethod
    def create_affiliate_link(
        db: Session,
        link_data: AffiliateLinkCreate
    ) -> AffiliateLink:
        """
        Create a new affiliate link.
        
        Args:
            db: Database session
            link_data: Affiliate link data
        
        Returns:
            Created AffiliateLink object
        
        Raises:
            ValueError: If product doesn't exist
        """
        # Verify product exists
        product = db.query(Product).filter(Product.id == link_data.product_id).first()
        if not product:
            raise ValueError(f"Product {link_data.product_id} not found")
        
        affiliate_link = AffiliateLink(
            product_id=link_data.product_id,
            platform=link_data.platform.lower(),
            affiliate_url=link_data.affiliate_url,
            product_sku=link_data.product_sku,
            commission_rate=link_data.commission_rate
        )
        
        db.add(affiliate_link)
        db.commit()
        db.refresh(affiliate_link)
        
        logger.info(f"Affiliate link created: {affiliate_link.id} for product {link_data.product_id}")
        return affiliate_link
    
    @staticmethod
    def get_affiliate_link_by_id(
        db: Session,
        link_id: int
    ) -> Optional[AffiliateLink]:
        """
        Get affiliate link by ID.
        
        Args:
            db: Database session
            link_id: Affiliate link ID
        
        Returns:
            AffiliateLink object or None
        """
        return db.query(AffiliateLink).filter(AffiliateLink.id == link_id).first()
    
    @staticmethod
    def get_affiliate_links_for_product(
        db: Session,
        product_id: int
    ) -> List[AffiliateLink]:
        """
        Get all affiliate links for a product.
        
        Args:
            db: Database session
            product_id: Product ID
        
        Returns:
            List of affiliate links
        """
        return db.query(AffiliateLink).filter(
            AffiliateLink.product_id == product_id,
            AffiliateLink.is_active == True
        ).all()
    
    @staticmethod
    def get_links_by_platform(
        db: Session,
        platform: str
    ) -> List[AffiliateLink]:
        """
        Get all active affiliate links for a platform.
        
        Args:
            db: Database session
            platform: Platform name (amazon, myntra, etc.)
        
        Returns:
            List of affiliate links
        """
        return db.query(AffiliateLink).filter(
            AffiliateLink.platform == platform.lower(),
            AffiliateLink.is_active == True
        ).all()
    
    @staticmethod
    def update_affiliate_link(
        db: Session,
        link_id: int,
        link_data: AffiliateLinkUpdate
    ) -> Optional[AffiliateLink]:
        """
        Update an affiliate link.
        
        Args:
            db: Database session
            link_id: Affiliate link ID
            link_data: Updated data
        
        Returns:
            Updated AffiliateLink object
        
        Raises:
            ValueError: If link not found
        """
        link = db.query(AffiliateLink).filter(AffiliateLink.id == link_id).first()
        if not link:
            raise ValueError(f"Affiliate link {link_id} not found")
        
        # Update fields if provided
        update_data = link_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(link, field, value)
        
        db.commit()
        db.refresh(link)
        
        logger.info(f"Affiliate link updated: {link_id}")
        return link
    
    @staticmethod
    def delete_affiliate_link(
        db: Session,
        link_id: int
    ) -> bool:
        """
        Delete an affiliate link (soft delete).
        
        Args:
            db: Database session
            link_id: Affiliate link ID
        
        Returns:
            True if successful
        
        Raises:
            ValueError: If link not found
        """
        link = db.query(AffiliateLink).filter(AffiliateLink.id == link_id).first()
        if not link:
            raise ValueError(f"Affiliate link {link_id} not found")
        
        link.is_active = False
        db.commit()
        
        logger.info(f"Affiliate link deleted: {link_id}")
        return True
    
    @staticmethod
    def get_all_platforms(db: Session) -> List[str]:
        """
        Get all active affiliate platforms.
        
        Args:
            db: Database session
        
        Returns:
            List of unique platform names
        """
        platforms = db.query(AffiliateLink.platform).filter(
            AffiliateLink.is_active == True
        ).distinct().all()
        return [p[0] for p in platforms]
    
    @staticmethod
    def bulk_create_affiliate_links(
        db: Session,
        links_data: List[AffiliateLinkCreate]
    ) -> List[AffiliateLink]:
        """
        Create multiple affiliate links at once.
        
        Args:
            db: Database session
            links_data: List of affiliate link data
        
        Returns:
            List of created links
        """
        created_links = []
        for link_data in links_data:
            try:
                link = AffiliateService.create_affiliate_link(db, link_data)
                created_links.append(link)
            except ValueError as e:
                logger.error(f"Failed to create affiliate link: {e}")
        
        return created_links
