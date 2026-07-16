from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# Activity Schemas
class ActivityBase(BaseModel):
    day_number: int
    name: str
    description: Optional[str] = None
    type: str  # hotel, breakfast, lunch, dinner, museum, event, attraction, transit, rest, coffee, sunset
    start_time: Optional[str] = None  # HH:MM
    end_time: Optional[str] = None    # HH:MM
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_website: Optional[str] = None
    contact_email: Optional[str] = None
    cost: float = 0.0
    rating: Optional[float] = None
    travel_distance_km: Optional[float] = None
    travel_duration_min: Optional[float] = None
    travel_mode: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: str
    trip_id: str

    class Config:
        from_attributes = True

# Trip Schemas
class TripBase(BaseModel):
    destination: str
    start_date: date
    end_date: date
    budget: float = 0.0
    num_travelers: int = 1
    status: str = "planning"

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    num_travelers: Optional[int] = None
    status: Optional[str] = None

class TripResponse(TripBase):
    id: str
    user_id: str
    created_at: datetime
    activities: List[ActivityResponse] = []

    class Config:
        from_attributes = True

# Saved Place Schemas
class SavedPlaceBase(BaseModel):
    place_id: Optional[str] = None
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[float] = None
    category: Optional[str] = None

class SavedPlaceCreate(SavedPlaceBase):
    pass

class SavedPlaceResponse(SavedPlaceBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True
