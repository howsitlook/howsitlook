"""
Database connection and session management.
Uses SQLite for local development with SQLAlchemy ORM.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging
from core.config import get_settings

logger = logging.getLogger(__name__)

# Get database URL from settings
settings = get_settings()
database_url = settings.database_url

# SQLite-specific engine configuration for local development
if "sqlite" in database_url:
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # For PostgreSQL or other databases
    engine = create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """
    Dependency to get database session for requests.
    Yields a session and ensures cleanup after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    Should be called once during app startup.
    """
    from schemas.base import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")


def drop_db():
    """
    Drop all tables. Use with caution!
    """
    from schemas.base import Base
    Base.metadata.drop_all(bind=engine)
    logger.warning("All database tables dropped!")
