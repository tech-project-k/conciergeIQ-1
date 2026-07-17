# =====================================================================
# Why it exists:
# Prevents duplicate, redundant calls to expensive external APIs (Google Maps, 
# OpenWeather) by caching requests.
#
# What it does:
# Stores query inputs and matching responses in a local key-value dictionary structure 
# with basic time-to-live (TTL) expiration logic.
#
# How it works:
# Standard Python dictionary lookup. Keys are hashed inputs; values store payloads 
# and timestamps.
#
# How it integrates:
# Imported by maps.py and weather.py. Before making a network request, they call 
# `cache.get(key)`. If a hit is found, it bypasses HTTP requests entirely.
# =====================================================================

import time
from typing import Any, Dict, Optional
from utils.logger import get_logger

logger = get_logger("cache_service")

class CacheService:
    """
    In-memory Cache service with basic TTL (Time-To-Live) expiration checks.
    """
    def __init__(self, default_ttl_seconds: int = 1800):
        """
        Initializes the cache mapping and default TTL (30 minutes).
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl_seconds
        logger.info(f"Local Cache Service initialized with default TTL of {self.default_ttl} seconds.")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from the cache if it exists and has not expired.
        
        Args:
            key (str): The unique cache key identifier.
            
        Returns:
            Optional[Any]: The cached payload, or None if expired/not found.
        """
        if key in self._cache:
            entry = self._cache[key]
            # Check if current time exceeds expiration threshold
            if time.time() < entry["expires_at"]:
                logger.info(f"Cache HIT for key: {key}")
                return entry["data"]
            else:
                logger.info(f"Cache EXPIRED for key: {key}")
                # Remove expired entry to free memory
                del self._cache[key]
        return None

    def set(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """
        Saves a payload in the cache mapping.
        
        Args:
            key (str): The unique cache key.
            data (Any): The payload to store.
            ttl (Optional[int]): Custom expiry in seconds. Falls back to default.
        """
        ttl_seconds = ttl if ttl is not None else self.default_ttl
        expires_at = time.time() + ttl_seconds
        self._cache[key] = {
            "data": data,
            "expires_at": expires_at
        }
        logger.info(f"Cache SET for key: {key} (Expires in {ttl_seconds}s)")

    def clear(self) -> None:
        """
        Wipes all entries from the cache.
        """
        self._cache.clear()
        logger.info("Local Cache cleared successfully.")

# Instantiated cache service singleton
cache_service = CacheService()
