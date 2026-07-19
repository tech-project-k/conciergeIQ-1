# =====================================================================
# Why it exists:
# Centralizes all configuration settings, defaults, and API keys for the 
# entire application. This avoids importing os.getenv across multiple files.
#
# What it does:
# Parses environment variables from `.env` using Pydantic Settings and 
# exposes a validated configurations object.
#
# How it works:
# Inherits from Pydantic's `BaseSettings` which reads variables from system env 
# and fallback `.env` files, automatically mapping them to strongly typed properties.
#
# How it integrates:
# Imported by routes, agents, services, and app.py to configure ports, 
# credentials, and operational modes.
# =====================================================================

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load env variables explicitly
load_dotenv()

class Settings(BaseSettings):
    """
    Settings model for loading configurations from environment variables or .env file.
    """
    # FastAPI Server configuration
    PORT: int = int(os.getenv("PORT", 8085))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # AI API Credentials
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # External APIs Keys
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    TICKETMASTER_API_KEY: str = os.getenv("TICKETMASTER_API_KEY", "")
    FOURSQUARE_API_KEY: str = os.getenv("FOURSQUARE_API_KEY", "")

    # SQLite Database connection string for chat history and caching
    DATABASE_URL: str = "sqlite:///./conciergeiq_genai.db"

    # Configurations mapping
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Instantiated settings singleton
settings = Settings()
