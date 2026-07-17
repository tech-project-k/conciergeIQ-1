# =====================================================================
# Why it exists:
# Main travel agent coordinator for ConciergeIQ.
# =====================================================================

from typing import Dict, Any, List
from agents.memory_agent import memory_agent
from agents.intent_agent import intent_agent
from agents.weather_agent import weather_agent
from agents.retriever_agent import retriever_agent
from agents.planner_agent import planner_agent
from agents.validator_agent import validator_agent
from agents.recommendation_agent import recommendation_agent
from agents.response_agent import response_agent
from models.schemas import ChatResponse, DailyItinerary
from utils.logger import get_logger

logger = get_logger("travel_agent")

class TravelAgent:
    def process_chat_message(self, session_id: str, message: str) -> ChatResponse:
        past_messages = memory_agent.load_chat_history(session_id)
        previous_preferences = memory_agent.load_preferences(session_id)
        
        preferences = intent_agent.extract_intent(message, previous_preferences)
        memory_agent.persist_preferences(session_id, preferences)
        
        destination = preferences.get("destination", "Unknown")
        budget = preferences.get("budget", 5000.0)
        
        if destination == "Unknown":
            response_text = "I would love to help you plan your next trip! Which city are you planning to visit? (e.g. Vizag, Hyderabad, Rajahmundry, or Ravulapalem)"
            memory_agent.save_chat_turn(session_id, message, response_text)
            return ChatResponse(
                session_id=session_id,
                response=response_text
            )

        weather_eval = weather_agent.evaluate_weather(destination)
        catalog_spots = retriever_agent.retrieve_context(destination, preferences.get("interests", []))
        raw_plan_text = planner_agent.generate_plan(preferences, catalog_spots, weather_eval["status"])
        
        date = preferences.get("start_date", "2026-07-18")
        itinerary = response_agent.format_response(raw_plan_text, "Guest", date, weather_eval["status"])
        validation = validator_agent.validate_itinerary(itinerary, budget, weather_eval["is_rainy"])
        
        itinerary_places = [item.activity_name for day in itinerary for item in day.schedule]
        recommendations = recommendation_agent.generate_recommendations(
            destination=destination,
            interests=preferences.get("interests", []),
            current_itinerary_places=itinerary_places,
            itinerary_text=raw_plan_text
        )
        
        warning_msg = ""
        if not validation["is_valid"]:
            warning_msg = f"\n\n⚠️ Alerts: " + " | ".join(validation["warnings"])
            
        response_text = (
            f"Here is your personalized itinerary for {destination}! "
            f"Estimated cost is Rs. {validation['estimated_cost']:.2f} (Budget Limit: Rs. {budget:.2f}). "
            f"Weather is currently {weather_eval['description']} ({weather_eval['temperature']})."
            f"{warning_msg}"
        )
        if recommendations:
            response_text += "\n\n💡 Recommendations:\n" + "\n".join(f"- {r}" for r in recommendations)

        memory_agent.save_chat_turn(session_id, message, response_text)
        
        return ChatResponse(
            session_id=session_id,
            response=response_text,
            itinerary=itinerary,
            estimated_cost=validation["estimated_cost"],
            travel_time="45 mins",
            weather_summary=f"{weather_eval['status']} ({weather_eval['temperature']})",
            booking_alerts=validation["warnings"]
        )

travel_agent = TravelAgent()
