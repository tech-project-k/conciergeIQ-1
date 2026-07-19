# =====================================================================
# Why it exists:
# Checks and monitors itinerary cost constraints.
# =====================================================================

from typing import Dict, Any, List
from models.schemas import DailyItinerary
from utils.logger import get_logger

logger = get_logger("budget_service")

class BudgetService:
    def __init__(self):
        logger.info("Budget Monitoring Service initialized.")

    def analyze_itinerary_budget(self, itinerary: List[DailyItinerary], limit: float) -> Dict[str, Any]:
        total_cost = 0.0
        for day in itinerary:
            for item in day.schedule:
                total_cost += item.cost
                
        remaining = limit - total_cost
        is_violated = total_cost > limit
        
        return {
            "total_estimated_cost": total_cost,
            "budget_limit": limit,
            "remaining_budget": remaining,
            "is_violated": is_violated,
            "message": "Budget checks passed successfully." if not is_violated else f"Budget violated! Cost of {total_cost} exceeds limit of {limit}."
        }

    def suggest_budget_reductions(self, itinerary: List[DailyItinerary]) -> List[str]:
        suggestions = []
        for day in itinerary:
            for item in day.schedule:
                if item.cost > 1000:
                    suggestions.append(f"Consider replacing '{item.activity_name}' ({item.cost}) with a free or lower-cost attraction.")
        return suggestions

budget_service = BudgetService()
