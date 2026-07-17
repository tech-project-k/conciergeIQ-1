# =====================================================================
# Why it exists:
# Exposes the POST /explore REST endpoint.
# =====================================================================

from fastapi import APIRouter, HTTPException
from models.schemas import ExploreRequest
from vector_db.store import vector_store

router = APIRouter(prefix="/explore", tags=["explore"])

@router.post("")
def explore_places(payload: ExploreRequest):
    try:
        results = vector_store.search_catalog(query=payload.place_type, city=payload.city)
        filtered = [r for r in results if r["type"].lower() == payload.place_type.lower()]
        return {"city": payload.city, "places": filtered}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
