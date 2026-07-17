# =====================================================================
# Why it exists:
# Booking reservations engine.
# =====================================================================

import uuid
from datetime import datetime
from typing import Dict, Any
from utils.logger import get_logger

logger = get_logger("booking_service")

class BookingService:
    def __init__(self):
        logger.info("Local Booking simulation engine online.")

    def pre_reserve_ticket(self, place_name: str, booking_type: str, cost: float, is_user_permission_granted: bool) -> Dict[str, Any]:
        booking_id = f"BK-{uuid.uuid4().hex[:8].upper()}"
        if is_user_permission_granted:
            status = f"CLAW-AUTO-{uuid.uuid4().hex[:6].upper()}"
            message = "Booking confirmed and payment processed automatically."
        else:
            status = "CLAW-PENDING"
            message = "Reservation locked. Waiting for user payment permission/approval."
            
        return {
            "booking_id": booking_id,
            "place_name": place_name,
            "booking_type": booking_type,
            "cost": cost,
            "confirmation_code": status,
            "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        }

booking_service = BookingService()
