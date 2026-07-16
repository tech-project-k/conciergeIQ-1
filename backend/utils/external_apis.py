import math
import requests
import logging
from typing import List, Dict, Any, Optional
from backend.config import settings
from backend.utils.mock_data import get_fallback_data

logger = logging.getLogger(__name__)

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in km between two coordinate points using haversine formula."""
    R = 6371.0 # Earth's radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def get_live_weather(lat: float, lon: float) -> Dict[str, Any]:
    """Fetch live weather details from OpenWeatherMap or return default sunny weather."""
    if settings.OPENWEATHER_API_KEY:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return {
                    "temp": data["main"]["temp"],
                    "condition": data["weather"][0]["main"], # Rain, Clear, Clouds, etc.
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"]
                }
        except Exception as e:
            logger.warning(f"Error fetching live weather: {e}")
            
    # Mock fallback
    return {
        "temp": 22.5,
        "condition": "Clear",
        "description": "sunny clear sky",
        "icon": "01d"
    }

def get_route_details(lat1: float, lon1: float, lat2: float, lon2: float, mode: str = "driving") -> Dict[str, Any]:
    """Estimate distance (km), travel duration (mins), and details between coordinates."""
    dist_km = haversine_distance(lat1, lon1, lat2, lon2)
    
    # Define average speed in km/h based on travel mode
    speeds = {
        "driving": 40.0,
        "transit": 25.0,
        "walking": 5.0,
        "bicycling": 15.0
    }
    
    speed = speeds.get(mode, 30.0)
    # duration in hours = distance / speed
    duration_hours = dist_km / speed
    duration_min = duration_hours * 60.0
    
    # Add a base buffer for traffic/stop lights/waiting time
    if mode == "transit":
        duration_min += 8.0 # wait time for train/bus
    elif mode == "driving":
        duration_min += 5.0 # traffic lights
    elif mode == "walking":
        duration_min += 2.0
        
    # Cap minimum values
    if dist_km < 0.1:
        dist_km = 0.1
        duration_min = 2.0
        
    return {
        "distance_km": round(dist_km, 2),
        "duration_min": round(duration_min, 1),
        "mode": mode
    }

def search_places_live(city: str, category: str) -> List[Dict[str, Any]]:
    """Retrieve hotels, restaurants, or attractions. Merges Google Places details or falls back to mock."""
    cleaned_city = city.lower().strip()
    fallback = get_fallback_data(cleaned_city)
    
    # Categorization map
    cat = category.lower().strip()
    
    # If Google Places API is configured, we could do live requests.
    # For safety & reliability in local setups, we query Google API if token exists; otherwise fallback
    if settings.GOOGLE_MAPS_API_KEY:
        try:
            # Simple text search query
            query = f"{category} in {city}"
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={settings.GOOGLE_MAPS_API_KEY}"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                results = res.json().get("results", [])
                places = []
                for r in results[:10]:
                    places.append({
                        "name": r.get("name"),
                        "address": r.get("formatted_address"),
                        "rating": r.get("rating", 4.0),
                        "coords": {
                            "lat": r.get("geometry", {}).get("location", {}).get("lat", 0.0),
                            "lon": r.get("geometry", {}).get("location", {}).get("lng", 0.0)
                        },
                        "place_id": r.get("place_id"),
                        "website": f"https://maps.google.com/?q={r.get('formatted_address')}",
                        "phone": "+33 1 00 00 00 00" # Placeholder phone, we fetch detail if needed
                    })
                if places:
                    return places
        except Exception as e:
            logger.warning(f"Error querying live Google Places: {e}")
            
    # Mock Database lookup based on query category
    if "hotel" in cat:
        return fallback.get("hotels", DEFAULT_CITY_PROFILE.get("hotels"))
    elif "restaurant" in cat or "food" in cat or "breakfast" in cat or "lunch" in cat or "dinner" in cat:
        return fallback.get("restaurants", DEFAULT_CITY_PROFILE.get("restaurants"))
    else:
        return fallback.get("attractions", DEFAULT_CITY_PROFILE.get("attractions"))
