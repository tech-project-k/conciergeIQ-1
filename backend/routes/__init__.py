from backend.routes.auth import router as auth_router
from backend.routes.trip import router as trip_router
from backend.routes.chat import router as chat_router
from backend.routes.places import router as places_router

__all__ = ["auth_router", "trip_router", "chat_router", "places_router"]
