from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.user import User
from backend.models.trip import Trip, SavedPlace
from backend.models.activity import Activity
from backend.schemas.trip import (
    TripCreate, TripUpdate, TripResponse, 
    ActivityCreate, ActivityResponse, 
    SavedPlaceCreate, SavedPlaceResponse
)
from backend.utils.security import get_current_user

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.get("", response_model=List[TripResponse])
def list_trips(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Trip).filter(Trip.user_id == current_user.id).order_by(Trip.created_at.desc()).all()

@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(trip_in: TripCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_trip = Trip(
        user_id=current_user.id,
        destination=trip_in.destination,
        start_date=trip_in.start_date,
        end_date=trip_in.end_date,
        budget=trip_in.budget,
        num_travelers=trip_in.num_travelers,
        status=trip_in.status
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return trip

@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: str,
    trip_in: TripUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        
    for field, value in trip_in.dict(exclude_unset=True).items():
        setattr(trip, field, value)
        
    db.commit()
    db.refresh(trip)
    return trip

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return None

# Activity Endpoints
@router.post("/{trip_id}/activities", response_model=ActivityResponse)
def add_activity(
    trip_id: str,
    act_in: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        
    new_act = Activity(
        trip_id=trip.id,
        **act_in.dict()
    )
    db.add(new_act)
    db.commit()
    db.refresh(new_act)
    return new_act

# Favorites / Saved Places
@router.post("/saved", response_model=SavedPlaceResponse)
def save_place(
    place_in: SavedPlaceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(SavedPlace).filter(
        SavedPlace.user_id == current_user.id,
        SavedPlace.name == place_in.name
    ).first()
    if existing:
        return existing
        
    new_place = SavedPlace(
        user_id=current_user.id,
        **place_in.dict()
    )
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place

@router.get("/saved", response_model=List[SavedPlaceResponse])
def get_saved_places(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SavedPlace).filter(SavedPlace.user_id == current_user.id).all()
