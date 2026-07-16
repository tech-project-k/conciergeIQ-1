from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from backend.database import get_db
from backend.models.user import User, Preference
from backend.models.trip import Trip
from backend.models.activity import Activity
from backend.models.chat import ChatHistory
from backend.schemas.chat import ChatQuery
from backend.ai.graph import run_travel_planner
from backend.utils.security import get_current_user
from backend.schemas.trip import TripResponse

router = APIRouter(prefix="/chat", tags=["AI Chat"])

@router.post("")
def handle_chat_message(
    payload: ChatQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = payload.query
    trip_id = payload.trip_id
    
    # 1. Load active trip if trip_id is provided or look for the most recent planning trip
    active_trip = None
    if trip_id:
        active_trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    else:
        active_trip = db.query(Trip).filter(Trip.user_id == current_user.id, Trip.status == "planning").order_by(Trip.created_at.desc()).first()
        
    # Prepare existing activities list to feed into LangGraph memory
    existing_activities = []
    if active_trip:
        for act in active_trip.activities:
            existing_activities.append({
                "day_number": act.day_number,
                "name": act.name,
                "description": act.description,
                "type": act.type,
                "start_time": act.start_time,
                "end_time": act.end_time,
                "latitude": act.latitude,
                "longitude": act.longitude,
                "address": act.address,
                "contact_phone": act.contact_phone,
                "contact_website": act.contact_website,
                "contact_email": act.contact_email,
                "cost": act.cost,
                "rating": act.rating,
                "travel_distance_km": act.travel_distance_km,
                "travel_duration_min": act.travel_duration_min,
                "travel_mode": act.travel_mode
            })
            
    # 2. Run LangGraph Workflow
    result = run_travel_planner(
        query=query,
        user_id=current_user.id,
        current_trip_id=active_trip.id if active_trip else None,
        existing_itinerary=existing_activities
    )
    
    intent = result.get("intent", "chat")
    response_text = result.get("response_text", "")
    itinerary_data = result.get("itinerary", [])
    warnings = result.get("optimization_warnings", [])
    
    # 3. Synchronize Trip & Activities back to the DB
    updated_trip_response = None
    destination = result.get("destination")
    
    if destination and (intent in ["plan", "modify"] or len(itinerary_data) > 0):
        # Determine dates
        start_date_str = result.get("start_date") or datetime.now().date().isoformat()
        end_date_str = result.get("end_date") or (datetime.now() + timedelta(days=2)).date().isoformat()
        
        try:
            start_d = datetime.strptime(start_date_str[:10], "%Y-%m-%d").date()
            end_d = datetime.strptime(end_date_str[:10], "%Y-%m-%d").date()
        except Exception:
            start_d = datetime.now().date()
            end_d = (datetime.now() + timedelta(days=2)).date()
            
        if not active_trip:
            # Create a brand new Trip
            active_trip = Trip(
                user_id=current_user.id,
                destination=destination,
                start_date=start_d,
                end_date=end_d,
                budget=result.get("budget", 0.0) or 500.0,
                num_travelers=result.get("num_travelers", 1),
                status="planning"
            )
            db.add(active_trip)
            db.commit()
            db.refresh(active_trip)
        else:
            # Update existing trip attributes
            active_trip.destination = destination
            active_trip.start_date = start_d
            active_trip.end_date = end_d
            if result.get("budget"):
                active_trip.budget = result.get("budget")
            db.commit()
            
        # Overwrite/update activities
        # For simplicity in plan syncing, delete old activities and insert fresh updated sequence
        db.query(Activity).filter(Activity.trip_id == active_trip.id).delete()
        db.commit()
        
        for idx, act in enumerate(itinerary_data):
            new_act = Activity(
                trip_id=active_trip.id,
                day_number=act.get("day_number", 1),
                name=act.get("name"),
                description=act.get("description"),
                type=act.get("type"),
                start_time=act.get("start_time"),
                end_time=act.get("end_time"),
                latitude=act.get("latitude"),
                longitude=act.get("longitude"),
                address=act.get("address"),
                contact_phone=act.get("contact_phone"),
                contact_website=act.get("contact_website"),
                contact_email=act.get("contact_email"),
                cost=act.get("cost", 0.0),
                rating=act.get("rating"),
                travel_distance_km=act.get("travel_distance_km"),
                travel_duration_min=act.get("travel_duration_min"),
                travel_mode=act.get("travel_mode")
            )
            db.add(new_act)
            
        db.commit()
        db.refresh(active_trip)
        updated_trip_response = TripResponse.from_orm(active_trip)
        
    # 4. Save Chat History
    user_msg = ChatHistory(
        user_id=current_user.id,
        trip_id=active_trip.id if active_trip else None,
        role="user",
        content=query
    )
    assistant_msg = ChatHistory(
        user_id=current_user.id,
        trip_id=active_trip.id if active_trip else None,
        role="assistant",
        content=response_text
    )
    db.add(user_msg)
    db.add(assistant_msg)
    db.commit()
    
    # 5. Fetch full messages history
    history = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id,
        ChatHistory.trip_id == (active_trip.id if active_trip else None)
    ).order_by(ChatHistory.timestamp.asc()).all()
    
    messages_list = []
    for msg in history:
        messages_list.append({
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        })
        
    return {
        "response_text": response_text,
        "trip": updated_trip_response,
        "warnings": warnings,
        "intent": intent,
        "messages": messages_list
    }

@router.get("/history/{trip_id}")
def get_chat_history(
    trip_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id,
        ChatHistory.trip_id == trip_id
    ).order_by(ChatHistory.timestamp.asc()).all()
    
    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        } for msg in history
    ]
