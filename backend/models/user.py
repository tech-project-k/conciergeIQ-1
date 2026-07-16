import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    preferences = relationship("Preference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Store dynamic interests and weights, e.g., {"adventure": 5, "nature": 2, "nightlife": 0}
    travel_style = Column(JSON, default=dict)
    
    # Food/diet preferences, e.g., ["vegetarian", "gluten-free"]
    dietary_restrictions = Column(JSON, default=list)
    
    # Needs such as "wheelchair access", "minimal walking"
    accessibility_needs = Column(JSON, default=list)
    
    # budget tier: "budget", "moderate", "luxury"
    budget_tier = Column(String(50), default="moderate")

    # Relationships
    user = relationship("User", back_populates="preferences")
