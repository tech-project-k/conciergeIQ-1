# =====================================================================
# Why it exists:
# Offers personalized regional suggestions.
# =====================================================================

from typing import List, Dict, Any
from utils.logger import get_logger

logger = get_logger("recommendations_service")

class RecommendationsService:
    def __init__(self):
        logger.info("Recommendation Service initialized.")

    def get_personalized_suggestions(self, destination: str, interests: List[str], current_itinerary_places: List[str]) -> List[Dict[str, Any]]:
        local_db = [
            {"city": "Vizag", "name": "Kailasagiri Hilltop Ropeway", "category": "Adventure", "rating": 4.6, "cost": 150.0},
            {"city": "Vizag", "name": "Simhachalam Temple", "category": "Culture", "rating": 4.8, "cost": 50.0},
            {"city": "Vizag", "name": "Yarada Beach (Hidden Gem)", "category": "Beach", "rating": 4.7, "cost": 0.0},
            {"city": "Hyderabad", "name": "Golconda Fort Sound & Light Show", "category": "Culture", "rating": 4.7, "cost": 150.0},
            {"city": "Hyderabad", "name": "Ramoji Film City Day Tour", "category": "Entertainment", "rating": 4.5, "cost": 1200.0},
            {"city": "Hyderabad", "name": "Birla Mandir Sunset Walk", "category": "Sightseeing", "rating": 4.8, "cost": 0.0},
            {"city": "Rajahmundry", "name": "Papikondalu Boat Cruise", "category": "Adventure", "rating": 4.8, "cost": 2500.0},
            {"city": "Rajahmundry", "name": "Kadiyam Nurseries Garden Tour", "category": "Nature", "rating": 4.6, "cost": 100.0},
            {"city": "Rajahmundry", "name": "Maredumilli Eco Tourism Forest", "category": "Adventure", "rating": 4.7, "cost": 200.0},
            {"city": "Ravulapalem", "name": "Gautami Bridge Sunset View Point", "category": "Nature", "rating": 4.8, "cost": 0.0},
            {"city": "Ravulapalem", "name": "Local Organic Coconut Groves Walk", "category": "Sightseeing", "rating": 4.6, "cost": 0.0}
        ]
        
        city_lower = destination.lower()
        filtered = [item for item in local_db if item["city"].lower() == city_lower]
        
        final_suggestions = []
        for item in filtered:
            if item["name"].lower() not in [p.lower() for p in current_itinerary_places]:
                match_score = 0
                for interest in interests:
                    if interest.lower() in item["category"].lower() or interest.lower() in item["name"].lower():
                        match_score += 1
                item["match_score"] = match_score
                final_suggestions.append(item)
                
        final_suggestions.sort(key=lambda x: (x["match_score"], x["rating"]), reverse=True)
        return final_suggestions[:3]

recommendations_service = RecommendationsService()
