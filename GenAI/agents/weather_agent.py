# =====================================================================
# Why it exists:
# Monitors weather forecast conditions.
# =====================================================================

from typing import Dict, Any
from services.weather import weather_service
from utils.logger import get_logger

logger = get_logger("weather_agent")

class WeatherAgent:
    def __init__(self):
        logger.info("Weather Agent initialized.")

    def evaluate_weather(self, city: str) -> Dict[str, Any]:
        forecast = weather_service.get_weather_forecast(city)
        if forecast["is_rainy"]:
            advice = "HEAVY RAIN FORECASTED: Prioritize INDOOR attractions (Museums, Dining) and avoid outdoor beach activities."
        else:
            advice = "CLEAR WEATHER: Great for OUTDOOR activities (Beach walks, Ropeways)."
        forecast["advice"] = advice
        return forecast

weather_agent = WeatherAgent()
