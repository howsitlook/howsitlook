"""
Helper script to create sample data for testing and demo.
Run: python scripts/seed_data.py
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from core.db import SessionLocal, init_db
from schemas.base import User, Product, AffiliateLink
from core.security import hash_password, UserRole
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_users():
    """Create sample users with different roles."""
    db = SessionLocal()
    
    users_data = [
        {
            "email": "admin@fashion.com",
            "username": "superadmin",
            "password": "admin123456",
            "full_name": "Admin User",
            "role": UserRole.SUPER_ADMIN
        },
        {
            "email": "content@fashion.com",
            "username": "contentmgr",
            "password": "content123456",
            "full_name": "Content Manager",
            "role": UserRole.CONTENT_MANAGER
        },
        {
            "email": "affiliate@fashion.com",
            "username": "affiliatemgr",
            "password": "affiliate123456",
            "full_name": "Affiliate Manager",
            "role": UserRole.AFFILIATE_MANAGER
        },
        {
            "email": "user@fashion.com",
            "username": "fashionuser",
            "password": "user123456",
            "full_name": "Fashion User",
            "role": UserRole.USER
        }
    ]
    
    for user_data in users_data:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            logger.info(f"User {user_data['email']} already exists")
            continue
        
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            hashed_password=hash_password(user_data["password"]),
            full_name=user_data["full_name"],
            role=user_data["role"],
            is_active=True,
            is_verified=True
        )
        db.add(user)
        logger.info(f"Created user: {user_data['email']} (role: {user_data['role']})")
    
    db.commit()
    db.close()


def seed_products():
    """Create sample products."""
    db = SessionLocal()
    
    products_data = [
        {
            "name": "Blue Cotton T-Shirt",
            "brand": "StyleCo",
            "category": "tops",
            "price": 29.99,
            "description": "Classic blue cotton t-shirt",
            "image_url": "https://via.placeholder.com/300?text=Blue+TShirt",
            "color": "blue",
            "fabric_type": "cotton",
            "tags": ["casual", "everyday", "summer"]
        },
        {
            "name": "Black Jeans",
            "brand": "DenimPro",
            "category": "bottoms",
            "price": 59.99,
            "description": "Comfortable black jeans",
            "image_url": "https://via.placeholder.com/300?text=Black+Jeans",
            "color": "black",
            "fabric_type": "denim",
            "tags": ["casual", "everyday", "classic"]
        },
        {
            "name": "White Summer Dress",
            "brand": "ElegantStyle",
            "category": "dresses",
            "price": 79.99,
            "description": "Light white summer dress",
            "image_url": "https://via.placeholder.com/300?text=White+Dress",
            "color": "white",
            "fabric_type": "cotton",
            "tags": ["summer", "dress", "casual"]
        },
        {
            "name": "Red Blazer",
            "brand": "FormalWear",
            "category": "outerwear",
            "price": 129.99,
            "description": "Professional red blazer",
            "image_url": "https://via.placeholder.com/300?text=Red+Blazer",
            "color": "red",
            "fabric_type": "wool",
            "tags": ["formal", "office", "professional"]
        },
        {
            "name": "Beige Cardigan",
            "brand": "CozyKnits",
            "category": "outerwear",
            "price": 69.99,
            "description": "Comfortable beige cardigan",
            "image_url": "https://via.placeholder.com/300?text=Beige+Cardigan",
            "color": "beige",
            "fabric_type": "wool",
            "tags": ["casual", "autumn", "layering"]
        }
    ]
    
    for product_data in products_data:
        existing = db.query(Product).filter(Product.name == product_data["name"]).first()
        if existing:
            logger.info(f"Product {product_data['name']} already exists")
            continue
        
        product = Product(
            name=product_data["name"],
            brand=product_data["brand"],
            category=product_data["category"],
            price=product_data["price"],
            description=product_data["description"],
            image_url=product_data["image_url"],
            color=product_data.get("color"),
            fabric_type=product_data.get("fabric_type"),
            tags=product_data.get("tags", []),
            is_active=True
        )
        db.add(product)
        logger.info(f"Created product: {product_data['name']}")
    
    db.commit()
    db.close()


def seed_affiliate_links():
    """Create sample affiliate links."""
    db = SessionLocal()
    
    # Get products
    products = db.query(Product).all()
    
    platforms = ["amazon", "myntra", "meesho", "ajio", "flipkart"]
    
    for product in products:
        existing = db.query(AffiliateLink).filter(
            AffiliateLink.product_id == product.id
        ).first()
        if existing:
            continue
        
        for platform in platforms[:2]:  # Add 2 platforms per product
            link = AffiliateLink(
                product_id=product.id,
                platform=platform,
                affiliate_url=f"https://{platform}.com/product-{product.id}",
                commission_rate=5.0,
                is_active=True
            )
            db.add(link)
            logger.info(f"Created affiliate link: {product.name} -> {platform}")
    
    db.commit()
    db.close()


def main():
    """Run all seed functions."""
    logger.info("Starting data seeding...")
    
    try:
        # Initialize database tables
        logger.info("Initializing database...")
        init_db()
        logger.info("✓ Database initialized")
        
        seed_users()
        logger.info("✓ Users seeded")
        
        seed_products()
        logger.info("✓ Products seeded")
        
        seed_affiliate_links()
        logger.info("✓ Affiliate links seeded")
        
        logger.info("\n✓ Data seeding completed successfully!")
        logger.info("\nSample Users:")
        logger.info("  - admin@fashion.com / admin123456 (Super Admin)")
        logger.info("  - content@fashion.com / content123456 (Content Manager)")
        logger.info("  - affiliate@fashion.com / affiliate123456 (Affiliate Manager)")
        logger.info("  - user@fashion.com / user123456 (Regular User)")
    
    except Exception as e:
        logger.error(f"Error during seeding: {e}")
        raise


if __name__ == "__main__":
    main()
