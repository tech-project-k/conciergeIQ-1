from backend.database import Base
from backend.models.user import User, Preference
from backend.models.trip import Trip, SavedPlace
from backend.models.activity import Activity
from backend.models.chat import ChatHistory

# Expose models for easier imports
__all__ = ["Base", "User", "Preference", "Trip", "SavedPlace", "Activity", "ChatHistory"]
