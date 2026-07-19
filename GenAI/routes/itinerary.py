# =====================================================================
# Why it exists:
# Exposes the POST /itinerary REST endpoint.
# =====================================================================

import uuid
from fastapi import APIRouter, HTTPException, status
from models.schemas import ItineraryRequest, ItineraryResponse
from agents.travel_agent import travel_agent
from utils.logger import get_logger

logger = get_logger("itinerary_router")

router = APIRouter(prefix="/itinerary", tags=["itinerary"])

@router.post("", response_model=ItineraryResponse, status_code=status.HTTP_200_OK)
def generate_itinerary(payload: ItineraryRequest):
    try:
        session_id = f"ITIN-{uuid.uuid4().hex[:6].upper()}"
        msg = f"Plan trip for {payload.guest_profile.destination}. Budget {payload.guest_profile.budget}."
        chat_response = travel_agent.process_chat_message(session_id, msg)
        return ItineraryResponse(
            guest_name=payload.guest_profile.name,
            destination=payload.guest_profile.destination,
            itinerary=chat_response.itinerary or [],
            estimated_cost=chat_response.estimated_cost,
            travel_time=chat_response.travel_time,
            weather=chat_response.weather_summary,
            recommendations=chat_response.booking_alerts,
            booking_status=False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
