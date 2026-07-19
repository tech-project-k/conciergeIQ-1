# =====================================================================
# Why it exists:
# Diagnostic check.
# =====================================================================

import sqlite3
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
def check_health():
    return {"status": "healthy", "service": "ConciergeIQ GenAI", "version": "1.0.0"}
