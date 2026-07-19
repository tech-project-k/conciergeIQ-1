# =====================================================================
# Why it exists:
# Saves and loads chat histories and preferences.
# =====================================================================

from typing import List, Dict, Any
from memory.manager import memory_manager
from utils.logger import get_logger

logger = get_logger("memory_agent")

class MemoryAgent:
    def load_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        return memory_manager.get_messages(session_id)

    def load_preferences(self, session_id: str) -> Dict[str, Any]:
        return memory_manager.get_preferences(session_id)

    def save_chat_turn(self, session_id: str, user_msg: str, assistant_msg: str) -> None:
        memory_manager.add_message(session_id, "user", user_msg)
        memory_manager.add_message(session_id, "assistant", assistant_msg)

    def persist_preferences(self, session_id: str, preferences: Dict[str, Any]) -> None:
        memory_manager.save_preferences(session_id, preferences)

    def clear_session_memory(self, session_id: str) -> None:
        memory_manager.clear_session(session_id)

memory_agent = MemoryAgent()
