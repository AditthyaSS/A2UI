"""Configuration management for Anti Gravity agent system."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Server configuration
    APP_NAME: str = "Anti Gravity Agent"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Agent configuration
    STREAM_DELAY: float = 0.1  # Delay between events for demonstration
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
