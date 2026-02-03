"""
Main FastAPI application entry point.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.config import get_settings
from core.db import init_db
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Fashion Virtual Try-On AI Backend API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = settings.avatar_upload_dir.split("/")[0]  # Get root static dir
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Import routers
from api.auth import router as auth_router
from api.products import router as products_router
from api.affiliate import router as affiliate_router
from api.tryon import router as tryon_router
from api.pose_transfer import router as pose_transfer_router
from api.recommendation import router as recommendation_router
from api.admin import router as admin_router

# Include routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(affiliate_router)
app.include_router(tryon_router)
app.include_router(pose_transfer_router)
app.include_router(recommendation_router)
app.include_router(admin_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on app startup."""
    logger.info("Starting Fashion Virtual Try-On API")
    init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on app shutdown."""
    logger.info("Shutting down Fashion Virtual Try-On API")


@app.get("/")
async def root():
    """Root endpoint - API status."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


@app.get("/api/v1/info")
async def api_info():
    """API information endpoint."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "ai_features": {
            "virtual_tryon": {
                "model": settings.vton_model_name,
                "status": "operational"
            },
            "pose_transfer": {
                "model": settings.pose_transfer_model,
                "status": "operational"
            },
            "recommendation": {
                "type": "CLIP + Fashion Rules",
                "status": "operational"
            }
        },
        "affiliate_platforms": [
            "amazon", "myntra", "meesho", "ajio", "flipkart"
        ],
        "max_recommendation": settings.recommendation_top_k
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
