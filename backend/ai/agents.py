import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from backend.config import settings
from backend.utils.external_apis import search_places_live, get_live_weather, get_route_details
from backend.ai.vector_db import vector_store

logger = logging.getLogger(__name__)

# Initialize LLM if configured
def get_llm():
    if settings.OPENAI_API_KEY:
        try:
            return ChatOpenAI(
                model="gpt-4o-mini",
                openai_api_key=settings.OPENAI_API_KEY,
                openai_api_base=settings.OPENAI_API_BASE,
                temperature=0.2
            )
        except Exception as e:
            logger.warning(f"Error initializing ChatOpenAI: {e}. Falling back to rule-based engine.")
    return None

def run_intent_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Parse user query to extract intent, destination, dates, budget, and styles."""
    query = state.get("query", "").lower()
    llm = get_llm()
    
    parsed = {
        "intent": "chat",
        "destination": state.get("destination"),
        "start_date": state.get("start_date"),
        "end_date": state.get("end_date"),
        "budget": state.get("budget", 0.0),
        "num_travelers": state.get("num_travelers", 1),
        "preferences": state.get("preferences", {})
    }
    
    # Check if there is an explicit request to plan or if keywords match
    plan_keywords = ["plan", "trip", "travel", "visit", "itinerary", "going to", "vacation"]
    modify_keywords = ["change", "move", "replace", "add", "avoid", "shift", "tomorrow", "cheaper"]
    
    if any(k in query for k in plan_keywords):
        parsed["intent"] = "plan"
    elif any(k in query for k in modify_keywords):
        parsed["intent"] = "modify"
        
    # Attempt simple rule-based parsing first
    # Extract destination
    words = query.split()
    for i, w in enumerate(words):
        if w in ["to", "in", "visit"] and i + 1 < len(words):
            dest = words[i+1].strip("?,.!")
            if dest not in ["a", "the", "my", "some", "our"]:
                parsed["destination"] = dest.capitalize()
                
    # If no destination found, default to Paris
    if not parsed["destination"]:
        if "paris" in query:
            parsed["destination"] = "Paris"
        elif "tokyo" in query:
            parsed["destination"] = "Tokyo"
            
    # Extract travelers, days, and budget
    if "kid" in query or "child" in query:
        parsed["preferences"]["has_kids"] = True
    if "senior" in query or "older" in query:
        parsed["preferences"]["has_seniors"] = True
    if "vegetarian" in query or "veg" in query:
        parsed["preferences"]["dietary"] = ["vegetarian"]
    if "adventure" in query:
        parsed["preferences"]["style"] = "adventure"
    elif "nature" in query:
        parsed["preferences"]["style"] = "nature"
    elif "luxury" in query:
        parsed["preferences"]["style"] = "luxury"
        
    # Standard values if planning
    if parsed["intent"] == "plan" and not parsed["start_date"]:
        parsed["start_date"] = datetime.now().date().isoformat()
        parsed["end_date"] = (datetime.now() + timedelta(days=3)).date().isoformat()
        
    # If LLM is available, refine parsing
    if llm:
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an AI Travel Intent Extractor. Parse the user's message and return a JSON object with: intent ('plan', 'modify', 'chat'), destination (string or null), start_date (YYYY-MM-DD or null), end_date (YYYY-MM-DD or null), budget (float), num_travelers (int), preferences (dictionary of travel styles, constraints). Respond ONLY with valid JSON."),
                ("user", "User Message: {query}\nCurrent State: {state_json}")
            ])
            chain = prompt | llm
            res = chain.invoke({"query": query, "state_json": json.dumps(parsed)})
            cleaned = res.content.strip().replace("```json", "").replace("```", "").strip()
            llm_parsed = json.loads(cleaned)
            parsed.update({k: v for k, v in llm_parsed.items() if v is not None})
        except Exception as e:
            logger.warning(f"LLM intent extraction failed: {e}. Using rule-based fallback.")

    # Return updated state slice
    return parsed

def run_search_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve live places, check weather, and query local RAG knowledge base."""
    destination = state.get("destination")
    if not destination:
        return {"live_places": [], "weather_info": {}, "rag_context": []}
        
    # 1. Fetch places for category (hotels, restaurants, attractions)
    hotels = search_places_live(destination, "hotels")
    restaurants = search_places_live(destination, "restaurants")
    attractions = search_places_live(destination, "attractions")
    
    all_places = hotels + restaurants + attractions
    
    # 2. Get Weather
    lat, lon = 48.8566, 2.3522  # Default to Paris
    if destination.lower() == "tokyo":
        lat, lon = 35.6762, 139.6503
        
    weather = get_live_weather(lat, lon)
    
    # 3. Query Vector Store (RAG)
    rag_results = vector_store.search(query=state.get("query", ""), city=destination, limit=3)
    rag_context = [d["text"] for d in rag_results]
    
    return {
        "live_places": all_places,
        "weather_info": weather,
        "rag_context": rag_context
    }

def run_planning_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Create the base itinerary connecting hotel, meals, and tourist attractions."""
    destination = state.get("destination")
    if not destination:
        return {"response_text": "I can plan a trip for you. Where would you like to travel?", "itinerary": []}
        
    places = state.get("live_places", [])
    if not places:
        # Re-fetch places if empty
        places = search_places_live(destination, "all")
        
    # Group places by type
    hotels = [p for p in places if p.get("website", "").find("hotel") != -1 or "hotel" in p.get("name", "").lower()]
    restaurants = [p for p in places if p.get("website", "").find("bistro") != -1 or "restaurant" in p.get("name", "").lower() or p.get("rating", 0) > 0 and p not in hotels]
    # Filter rest as attractions
    attractions = [p for p in places if p not in hotels and p not in restaurants]
    
    if not hotels:
        hotels = [{"name": f"Grand Central Hotel {destination}", "coords": {"lat": 48.858, "lon": 2.33}, "address": f"10 Main St, {destination}", "phone": "+1 234-567-890", "website": "http://example.com"}]
    if not restaurants:
        restaurants = [{"name": "Local Cafe", "coords": {"lat": 48.86, "lon": 2.34}, "address": f"12 Bistro Rd, {destination}", "phone": "+1 234-567-891", "website": "http://example.com"}]
    if not attractions:
        attractions = [{"name": f"{destination} Scenic Spot", "coords": {"lat": 48.87, "lon": 2.35}, "address": f"100 Viewpoint, {destination}", "phone": "+1 234-567-892", "website": "http://example.com"}]

    hotel = hotels[0]
    
    start_str = state.get("start_date") or datetime.now().date().isoformat()
    end_str = state.get("end_date") or (datetime.now() + timedelta(days=3)).date().isoformat()
    
    try:
        start_d = datetime.strptime(start_str, "%Y-%m-%d")
        end_d = datetime.strptime(end_str, "%Y-%m-%d")
        num_days = max(1, (end_d - start_d).days + 1)
    except:
        num_days = 3
        
    itinerary = []
    
    # Generate schedule day-by-day
    for day in range(1, num_days + 1):
        day_activities = []
        
        # 1. Hotel check-in / start of day
        day_activities.append({
            "day_number": day,
            "name": f"Hotel Departure: {hotel['name']}",
            "type": "hotel",
            "start_time": "08:30",
            "end_time": "09:00",
            "latitude": hotel["coords"]["lat"],
            "longitude": hotel["coords"]["lon"],
            "address": hotel["address"],
            "contact_phone": hotel.get("phone"),
            "contact_website": hotel.get("website"),
            "cost": 0.0,
            "description": "Start the day from the hotel."
        })
        
        # 2. Morning Attraction
        att1 = attractions[(day - 1) % len(attractions)]
        day_activities.append({
            "day_number": day,
            "name": att1["name"],
            "type": "attraction",
            "start_time": "09:30",
            "end_time": "12:00",
            "latitude": att1["coords"]["lat"],
            "longitude": att1["coords"]["lon"],
            "address": att1.get("address"),
            "contact_phone": att1.get("phone"),
            "contact_website": att1.get("website"),
            "cost": att1.get("price", 15.0),
            "description": "Explore the historic landmark and exhibits."
        })
        
        # 3. Lunch break
        lunch = restaurants[(day - 1) % len(restaurants)]
        day_activities.append({
            "day_number": day,
            "name": f"Lunch at {lunch['name']}",
            "type": "lunch",
            "start_time": "12:30",
            "end_time": "14:00",
            "latitude": lunch["coords"]["lat"],
            "longitude": lunch["coords"]["lon"],
            "address": lunch.get("address"),
            "contact_phone": lunch.get("phone"),
            "contact_website": lunch.get("website"),
            "cost": lunch.get("price", 25.0),
            "description": "Enjoy authentic local cuisine for lunch."
        })
        
        # 4. Afternoon activity (Museum or landmark)
        att2 = attractions[(day) % len(attractions)]
        day_activities.append({
            "day_number": day,
            "name": att2["name"],
            "type": "museum" if day % 2 == 0 else "attraction",
            "start_time": "14:30",
            "end_time": "17:00",
            "latitude": att2["coords"]["lat"],
            "longitude": att2["coords"]["lon"],
            "address": att2.get("address"),
            "contact_phone": att2.get("phone"),
            "contact_website": att2.get("website"),
            "cost": att2.get("price", 10.0),
            "description": "Guided walking tour and sightseeing."
        })
        
        # 5. Rest / Coffee break
        day_activities.append({
            "day_number": day,
            "name": "Mid-Afternoon Coffee Break",
            "type": "coffee",
            "start_time": "17:15",
            "end_time": "18:00",
            "latitude": att2["coords"]["lat"] + 0.002,
            "longitude": att2["coords"]["lon"] - 0.002,
            "address": "Local Cafe Shop nearby",
            "cost": 5.0,
            "description": "Rest and recharge with coffee and pastries."
        })
        
        # 6. Dinner
        dinner = restaurants[(day) % len(restaurants)]
        day_activities.append({
            "day_number": day,
            "name": f"Dinner at {dinner['name']}",
            "type": "dinner",
            "start_time": "19:00",
            "end_time": "21:00",
            "latitude": dinner["coords"]["lat"],
            "longitude": dinner["coords"]["lon"],
            "address": dinner.get("address"),
            "contact_phone": dinner.get("phone"),
            "contact_website": dinner.get("website"),
            "cost": dinner.get("price", 40.0),
            "description": "Relaxing dinner service."
        })
        
        # 7. Return to Hotel
        day_activities.append({
            "day_number": day,
            "name": f"Return to {hotel['name']}",
            "type": "hotel",
            "start_time": "21:30",
            "end_time": "22:00",
            "latitude": hotel["coords"]["lat"],
            "longitude": hotel["coords"]["lon"],
            "address": hotel["address"],
            "cost": 0.0,
            "description": "End of day. Rest at hotel."
        })
        
        itinerary.extend(day_activities)
        
    return {
        "itinerary": itinerary,
        "response_text": f"I've generated a complete, customized {num_days}-day travel itinerary for {destination}! Let me know if you would like me to adjust hotels, restaurants, or add specific activities."
    }

def run_optimization_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate distances, routing paths, EAT/ETA, and traffic impact for each step."""
    itinerary = state.get("itinerary", [])
    warnings = []
    
    if not itinerary:
        return {"itinerary": [], "optimization_warnings": []}
        
    optimized_activities = []
    
    # Group activities by day_number
    days_dict: Dict[int, List[Dict[str, Any]]] = {}
    for act in itinerary:
        day = act.get("day_number", 1)
        if day not in days_dict:
            days_dict[day] = []
        days_dict[day].append(act)
        
    for day, activities in days_dict.items():
        # Sort activities by start_time
        activities.sort(key=lambda x: x.get("start_time", ""))
        
        # Connect distances from previous activity
        for idx in range(len(activities)):
            act = activities[idx].copy()
            
            if idx == 0:
                # First activity starts at the hotel, no distance from previous needed
                act["travel_distance_km"] = 0.0
                act["travel_duration_min"] = 0.0
                act["travel_mode"] = "walking"
            else:
                prev = activities[idx - 1]
                lat1, lon1 = prev.get("latitude"), prev.get("longitude")
                lat2, lon2 = act.get("latitude"), act.get("longitude")
                
                if lat1 and lon1 and lat2 and lon2:
                    # Choose travel mode
                    dist_simple = abs(lat1-lat2) + abs(lon1-lon2)
                    mode = "walking"
                    if dist_simple > 0.02: # roughly > 2km
                        mode = "driving" # cab
                    elif dist_simple > 0.005:
                        mode = "transit" # subway/bus
                        
                    route = get_route_details(lat1, lon1, lat2, lon2, mode=mode)
                    act["travel_distance_km"] = route["distance_km"]
                    act["travel_duration_min"] = route["duration_min"]
                    act["travel_mode"] = route["mode"]
                    
                    # Check for travel conflicts (e.g. travel duration exceeds gap between start times)
                    # For example, if previous ends at 12:00, and current starts at 12:30, and travel takes 40 mins
                    # This would raise a schedule warning!
                    gap = 30.0 # Default 30 min buffer
                    if route["duration_min"] > gap:
                        warnings.append(f"Day {day}: Travel from {prev['name']} to {act['name']} takes {route['duration_min']} mins, which exceeds your planned break time.")
                else:
                    act["travel_distance_km"] = 0.0
                    act["travel_duration_min"] = 0.0
                    act["travel_mode"] = "walking"
                    
            optimized_activities.append(act)
            
    # Apply weather modifications if rain is forecast
    weather = state.get("weather_info", {})
    if weather.get("condition") == "Rain":
        warnings.append("Weather alert: Rain is forecast. We suggest moving outdoor walking tours indoors or packing an umbrella.")
        # Modify activity descriptions to include indoor warnings
        for act in optimized_activities:
            if act["type"] in ["attraction", "park"] and "indoor" not in act.get("description", "").lower():
                act["description"] = f"[Rain Alert: Plan Indoor Alternate] {act.get('description', '')}"
                
    return {
        "itinerary": optimized_activities,
        "optimization_warnings": warnings
    }
