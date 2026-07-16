import os
import sys

# Ensure the root project directory is in the python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import engine, Base
from backend.routes.auth import router as auth_router
from backend.routes.trip import router as trip_router
from backend.routes.chat import router as chat_router
from backend.routes.places import router as places_router

# Auto-create tables (SQLite or postgresql) on startup
# This ensures zero-friction startup for testing
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI Travel Concierge Platform",
    version="1.0.0",
    debug=settings.DEBUG
)

# Set up CORS to allow React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict to actual host
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(auth_router, prefix="/api")
app.include_router(trip_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(places_router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
