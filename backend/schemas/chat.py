from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatQuery(BaseModel):
    query: str
    trip_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    id: str
    user_id: str
    trip_id: Optional[str] = None
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]
