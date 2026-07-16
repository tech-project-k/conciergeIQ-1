import os
import math
import logging
from typing import List, Dict, Any, Optional
from backend.config import settings

logger = logging.getLogger(__name__)

# Preloaded local travel guide and emergency knowledge base
TRAVEL_KNOWLEDGE_BASE = [
    # Paris Guides
    {
        "city": "paris",
        "category": "safety",
        "text": "Paris is generally safe, but watch out for pickpockets near the Eiffel Tower, Louvre, and Sacre-Coeur. Keep your belongings secure in crowded metro cars."
    },
    {
        "city": "paris",
        "category": "emergency",
        "text": "Emergency Contacts in Paris: General Emergency (112), Police (17), Ambulance/SAMU (15). The American Hospital of Paris is at 63 Boulevard Victor Hugo, Neuilly-sur-Seine (Phone: +33 1 46 41 25 25)."
    },
    {
        "city": "paris",
        "category": "tips",
        "text": "For budget travel in Paris, buy a Navigo Decouverte weekly transit card. Avoid sit-down cafes right next to major monuments where prices are doubled."
    },
    {
        "city": "paris",
        "category": "hidden_gems",
        "text": "La Petite Ceinture is an abandoned railway line encircling Paris that has been converted into a lush, quiet nature walkway. Great for a peaceful escape."
    },
    # Tokyo Guides
    {
        "city": "tokyo",
        "category": "safety",
        "text": "Tokyo is one of the safest cities in the world. Crime is extremely low, but always note the nearest Koban (police box) if you lose something."
    },
    {
        "city": "tokyo",
        "category": "emergency",
        "text": "Emergency Contacts in Tokyo: Police (110), Fire/Ambulance (119). St. Luke's International Hospital is a popular English-speaking emergency hospital in Chuo City (+81 3-3541-5151)."
    },
    {
        "city": "tokyo",
        "category": "tips",
        "text": "Get a Pasmo or Suica IC card for easy tap-and-go travel on all subways and buses. Many places are cash-only, so always keep some Japanese Yen."
    },
    {
        "city": "tokyo",
        "category": "hidden_gems",
        "text": "Todoroki Valley is a hidden jungle ravine right in Setagaya ward. It is a cooler, forested walking path with a small temple and red bridge."
    }
]

class VectorStore:
    def __init__(self):
        self.documents = TRAVEL_KNOWLEDGE_BASE
        
    def _get_token_frequencies(self, text: str) -> Dict[str, int]:
        """Convert text into lowercase word tokens and count frequencies."""
        words = text.lower().replace(".", "").replace(",", "").replace(":", "").split()
        freq = {}
        for w in words:
            if len(w) > 3: # Ignore small stop words
                freq[w] = freq.get(w, 0) + 1
        return freq

    def _cosine_similarity(self, dict1: Dict[str, int], dict2: Dict[str, int]) -> float:
        """Simple cosine similarity over token frequency dicts."""
        intersection = set(dict1.keys()) & set(dict2.keys())
        numerator = sum([dict1[x] * dict2[x] for x in intersection])
        
        sum1 = sum([dict1[x]**2 for x in dict1.keys()])
        sum2 = sum([dict2[x]**2 for x in dict2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        if not denominator:
            return 0.0
        return numerator / denominator

    def add_document(self, city: str, category: str, text: str):
        self.documents.append({
            "city": city.lower().strip(),
            "category": category.lower().strip(),
            "text": text
        })

    def search(self, query: str, city: Optional[str] = None, limit: int = 3) -> List[Dict[str, Any]]:
        """Search the knowledge base using semantic/token similarity."""
        query_freq = self._get_token_frequencies(query)
        scored_docs = []
        
        for doc in self.documents:
            # Filter by city if specified
            if city and doc["city"] != city.lower().strip():
                continue
                
            doc_freq = self._get_token_frequencies(doc["text"])
            similarity = self._cosine_similarity(query_freq, doc_freq)
            
            # Boost score slightly if category keyword matches query
            if doc["category"] in query.lower():
                similarity += 0.2
                
            scored_docs.append((similarity, doc))
            
        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Return top matches with a positive match score or high relevance
        results = []
        for score, doc in scored_docs[:limit]:
            results.append({
                "city": doc["city"],
                "category": doc["category"],
                "text": doc["text"],
                "score": round(score, 4)
            })
        return results

# Singleton instance
vector_store = VectorStore()
