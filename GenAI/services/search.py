# =====================================================================
# Why it exists:
# Live query lookups.
# =====================================================================

from typing import List, Dict, Any
from utils.logger import get_logger

logger = get_logger("search_service")

class SearchService:
    def __init__(self):
        logger.info("Search Service initialized.")

    def run_live_search(self, query: str) -> List[Dict[str, str]]:
        query_lower = query.lower()
        if "vizag" in query_lower or "visakhapatnam" in query_lower:
            return [
                {
                    "title": "Vizag Travel Advisory",
                    "snippet": "Rushikonda Beach is fully open for water sports including speedboating. Navy museum timings are 2 PM to 8 PM.",
                    "url": "https://vizagtravel.org/advisory"
                }
            ]
        elif "hyderabad" in query_lower:
            return [
                {
                    "title": "Charminar Monument Updates",
                    "snippet": "Charminar opening hours are 9:30 AM to 5:30 PM. Weekend traffic around Laad Bazaar is high.",
                    "url": "https://hyderabadhistory.com/charminar"
                }
            ]
        return [
            {
                "title": "ConciergeIQ Travel Tips",
                "snippet": "Pre-booking entry tickets for popular temples is recommended.",
                "url": "https://conciergeiq.com/travel-tips"
            }
        ]

search_service = SearchService()
