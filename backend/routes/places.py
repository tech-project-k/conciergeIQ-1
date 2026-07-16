from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from backend.utils.external_apis import search_places_live, get_live_weather
from backend.utils.security import get_current_user
from backend.models.user import User

router = APIRouter(prefix="/places", tags=["Places & Weather"])

@router.get("/search")
def search_places(
    city: str,
    category: str = "attractions",
    current_user: User = Depends(get_current_user)
):
    """Search Google Places with fallbacks."""
    return search_places_live(city, category)

@router.get("/weather")
def get_weather(
    lat: float,
    lon: float,
    current_user: User = Depends(get_current_user)
):
    """Retrieve weather forecast."""
    return get_live_weather(lat, lon)
