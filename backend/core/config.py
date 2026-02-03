"""
Core configuration for the FastAPI application.
Handles environment variables and app settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    app_name: str = "Fashion Virtual Try-On API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./fashion_app.db"
    
    # JWT
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Paths
    avatar_upload_dir: str = "./static/avatars"
    input_dir: str = "./static/inputs"
    output_dir: str = "./static/outputs"
    
    # ML Models
    use_gpu: bool = False
    model_device: str = "cpu"  # cpu or cuda
    
    # API
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # AI Settings
    vton_model_name: str = "hr-vton"  # hr-vton or cp-vton
    pose_transfer_model: str = "pg2"  # pg2 or hr-vton-pose
    recommendation_top_k: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
