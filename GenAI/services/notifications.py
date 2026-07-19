# =====================================================================
# Why it exists:
# Notification alert manager.
# =====================================================================

from typing import List
from models.schemas import DailyItinerary
from utils.logger import get_logger

logger = get_logger("notifications_service")

class NotificationsService:
    def __init__(self):
        logger.info("Notification Service online.")

    def generate_itinerary_alerts(self, itinerary: List[DailyItinerary], is_rainy: bool) -> List[str]:
        alerts = []
        for day in itinerary:
            for item in day.schedule:
                if is_rainy and item.activity_type == "attraction":
                    outdoor_keywords = ["beach", "park", "ropeway", "cruise", "island", "outdoor"]
                    if any(kw in item.activity_name.lower() for kw in outdoor_keywords):
                        alerts.append(
                            f"Weather Alert: Rain is forecast. We recommend replacing outdoor activity "
                            f"'{item.activity_name}' with an indoor sight."
                        )
                ticket_keywords = ["temple", "museum", "imax", "multiplex", "event", "show", "concert"]
                if any(kw in item.activity_name.lower() for kw in ticket_keywords):
                    if item.cost > 0:
                        alerts.append(
                            f"Reservation Warning: '{item.activity_name}' requires entry tickets ({item.cost}). "
                            f"Tap 'Secure Reservation' to book now."
                        )
        return alerts

notifications_service = NotificationsService()
