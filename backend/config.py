import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "ConciergeIQ"
    DEBUG: bool = True
    
    # Database
    # Default to local SQLite database in current working directory
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./conciergeiq.db")
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretconciergeiqjwttokenkey123!#")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # External APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    class Config:
        case_sensitive = True

settings = Settings()
