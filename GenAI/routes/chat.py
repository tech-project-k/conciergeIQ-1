# =====================================================================
# Why it exists:
# Exposes the POST /chat REST endpoint.
# =====================================================================

from fastapi import APIRouter, HTTPException, status
from models.schemas import ChatRequest, ChatResponse
from agents.travel_agent import travel_agent
from utils.logger import get_logger

logger = get_logger("chat_router")

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def process_chat(payload: ChatRequest):
    logger.info(f"POST /api/chat received request for session: {payload.session_id}")
    try:
        response = travel_agent.process_chat_message(
            session_id=payload.session_id,
            message=payload.message
        )
        return response
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
