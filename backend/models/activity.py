import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String(36), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False) # Day 1, Day 2, etc.
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Category: hotel, breakfast, lunch, dinner, museum, event, attraction, coffee, transit, rest, etc.
    type = Column(String(100), nullable=False) 
    
    # Store times as standard 'HH:MM' string for SQLite / Postgres portability
    start_time = Column(String(10), nullable=True) 
    end_time = Column(String(10), nullable=True) 
    
    # Location coordinates & addresses
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String(500), nullable=True)
    
    # Contact assistance info
    contact_phone = Column(String(100), nullable=True)
    contact_website = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    
    # Budget optimization info
    cost = Column(Float, default=0.0)
    rating = Column(Float, nullable=True)
    
    # Intelligent transit planning details from previous activity (or airport/station)
    travel_distance_km = Column(Float, nullable=True)
    travel_duration_min = Column(Float, nullable=True)
    travel_mode = Column(String(50), nullable=True) # driving, transit, walking, bicycling
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    trip = relationship("Trip", back_populates="activities")
