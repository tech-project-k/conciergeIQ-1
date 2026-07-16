from datetime import datetime, timedelta
from typing import Optional, Any
import jwt
from jwt import PyJWTError as JWTError
# CryptContext removed (using raw bcrypt directly to fix Python 3.11+ passlib compatibility bug)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.config import settings
from backend.database import get_db
from backend.models.user import User

import bcrypt

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db)) -> User:
    from backend.models.user import Preference
    user = db.query(User).filter(User.email == "default@conciergeiq.com").first()
    if not user:
        user = User(
            email="default@conciergeiq.com",
            hashed_password="not_applicable",
            full_name="Default Traveler"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        pref = Preference(user_id=user.id)
        db.add(pref)
        db.commit()
        db.refresh(user)
    return user
