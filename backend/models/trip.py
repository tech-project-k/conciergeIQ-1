import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    destination = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Float, default=0.0)
    num_travelers = Column(Integer, default=1)
    status = Column(String(50), default="planning") # planning, active, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="trips")
    activities = relationship("Activity", back_populates="trip", cascade="all, delete-orphan")


class SavedPlace(Base):
    __tablename__ = "saved_places"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    place_id = Column(String(255), nullable=True) # Google Maps place_id
    name = Column(String(255), nullable=False)
    address = Column(String(500), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    category = Column(String(100), nullable=True) # hotel, restaurant, attraction, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
