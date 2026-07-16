from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List, Any
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Preferences Schemas
class PreferenceBase(BaseModel):
    travel_style: Dict[str, int] = Field(default_factory=dict, description="Style preferences like adventure, nature, etc. and their ratings 0-5")
    dietary_restrictions: List[str] = Field(default_factory=list, description="Dietary restrictions like vegetarian, gluten-free, etc.")
    accessibility_needs: List[str] = Field(default_factory=list, description="Accessibility needs")
    budget_tier: str = Field(default="moderate", description="budget, moderate, or luxury")

class PreferenceUpdate(PreferenceBase):
    pass

class PreferenceResponse(PreferenceBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    preferences: Optional[PreferenceResponse] = None

    class Config:
        from_attributes = True
