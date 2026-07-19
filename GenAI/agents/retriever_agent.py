# =====================================================================
# Why it exists:
# Fetches local sights matching user interests.
# =====================================================================

from typing import List, Dict, Any
from vector_db.store import vector_store
from utils.logger import get_logger

logger = get_logger("retriever_agent")

class RetrieverAgent:
    def __init__(self):
        logger.info("Retriever Agent initialized.")

    def retrieve_context(self, destination: str, interests: List[str]) -> List[Dict[str, Any]]:
        if not destination or destination == "Unknown":
            return []
        query = " ".join(interests)
        return vector_store.search_catalog(query=query, city=destination, limit=8)

retriever_agent = RetrieverAgent()
