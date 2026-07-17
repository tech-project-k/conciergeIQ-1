# =====================================================================
# Why it exists:
# Exposes the GET /recommendations endpoint.
# =====================================================================

from fastapi import APIRouter, Query, HTTPException
from typing import List
from services.recommendations import recommendations_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("")
def get_recommendations(destination: str = Query(...), interests: List[str] = Query([])):
    try:
        recs = recommendations_service.get_personalized_suggestions(destination, interests, [])
        return {"destination": destination, "recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
