# =====================================================================
# Why it exists:
# Audits itineraries against physical constraints.
# =====================================================================

from typing import List, Dict, Any
from models.schemas import DailyItinerary
from agents.budget_agent import budget_agent
from services.notifications import notifications_service
from utils.logger import get_logger

logger = get_logger("validator_agent")

class ValidatorAgent:
    def validate_itinerary(self, itinerary: List[DailyItinerary], budget_limit: float, is_rainy: bool) -> Dict[str, Any]:
        warnings = []
        
        # Budget check
        budget_audit = budget_agent.check_budget_compliance(itinerary, budget_limit)
        if budget_audit["is_violated"]:
            warnings.append(budget_audit["message"])

        # Weather check
        weather_alerts = notifications_service.generate_itinerary_alerts(itinerary, is_rainy)
        warnings.extend(weather_alerts)

        # Slots & Dups check
        visited = set()
        for day in itinerary:
            slots = []
            for item in day.schedule:
                if item.activity_name in visited:
                    warnings.append(f"Duplicate place: '{item.activity_name}' is scheduled multiple times.")
                visited.add(item.activity_name)
                if item.time_slot in slots:
                    warnings.append(f"Conflict: Multiple activities at '{item.time_slot}'.")
                slots.append(item.time_slot)

        return {
            "is_valid": len(warnings) == 0,
            "warnings": warnings,
            "estimated_cost": budget_audit["total_estimated_cost"]
        }

validator_agent = ValidatorAgent()
