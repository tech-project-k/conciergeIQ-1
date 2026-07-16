import logging
from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END

# Import agent nodes
from backend.ai.agents import run_intent_agent, run_search_agent, run_planning_agent, run_optimization_agent

logger = logging.getLogger(__name__)

# State structure
class PlanState(TypedDict):
    query: str
    user_id: str
    trip_id: Optional[str]
    messages: List[Dict[str, Any]]
    
    # Target inputs
    destination: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    budget: float
    num_travelers: int
    preferences: Dict[str, Any]
    
    # Retrieved helpers
    live_places: List[Dict[str, Any]]
    weather_info: Dict[str, Any]
    rag_context: List[str]
    
    # Outputs
    itinerary: List[Dict[str, Any]]
    optimization_warnings: List[str]
    intent: str
    response_text: str

# Define nodes for the workflow
def intent_node(state: PlanState) -> Dict[str, Any]:
    logger.info("Executing Intent Node")
    return run_intent_agent(state)

def search_node(state: PlanState) -> Dict[str, Any]:
    logger.info("Executing Search Node")
    return run_search_agent(state)

def planning_node(state: PlanState) -> Dict[str, Any]:
    logger.info("Executing Planning Node")
    return run_planning_agent(state)

def optimization_node(state: PlanState) -> Dict[str, Any]:
    logger.info("Executing Optimization Node")
    return run_optimization_agent(state)

def response_routing(state: PlanState) -> str:
    """Decide next steps based on user intent."""
    intent = state.get("intent")
    if intent == "plan":
        return "search"
    elif intent == "modify":
        return "optimization"
    else:
        return "planning"

# Construct State Graph
workflow = StateGraph(PlanState)

# Add Nodes
workflow.add_node("determine_intent", intent_node)
workflow.add_node("search", search_node)
workflow.add_node("planning", planning_node)
workflow.add_node("optimization", optimization_node)

# Set entry point
workflow.set_entry_point("determine_intent")

# Add conditional routing edges
workflow.add_conditional_edges(
    "determine_intent",
    response_routing,
    {
        "search": "search",
        "optimization": "optimization",
        "planning": "planning"
    }
)

# Connect linear paths
workflow.add_edge("search", "planning")
workflow.add_edge("planning", "optimization")
workflow.add_edge("optimization", END)

# Compile
app = workflow.compile()

def run_travel_planner(query: str, user_id: str, current_trip_id: Optional[str] = None, existing_itinerary: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Execute the full LangGraph travel agent loop."""
    initial_state: PlanState = {
        "query": query,
        "user_id": user_id,
        "trip_id": current_trip_id,
        "messages": [],
        
        "destination": None,
        "start_date": None,
        "end_date": None,
        "budget": 0.0,
        "num_travelers": 1,
        "preferences": {},
        
        "live_places": [],
        "weather_info": {},
        "rag_context": [],
        
        "itinerary": existing_itinerary or [],
        "optimization_warnings": [],
        "intent": "chat",
        "response_text": ""
    }
    
    # Run the compiled graph synchronously
    result = app.invoke(initial_state)
    return result
