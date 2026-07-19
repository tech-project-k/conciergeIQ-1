# =====================================================================
# Why it exists:
# Checks budget compliance.
# =====================================================================

from typing import Dict, Any, List
from models.schemas import DailyItinerary
from services.budget import budget_service
from utils.logger import get_logger

logger = get_logger("budget_agent")

class BudgetAgent:
    def check_budget_compliance(self, itinerary: List[DailyItinerary], budget_limit: float) -> Dict[str, Any]:
        analysis = budget_service.analyze_itinerary_budget(itinerary, budget_limit)
        if analysis["is_violated"]:
            analysis["cost_reduction_tips"] = budget_service.suggest_budget_reductions(itinerary)
        else:
            analysis["cost_reduction_tips"] = []
        return analysis

budget_agent = BudgetAgent()
