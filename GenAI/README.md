# ConciergeIQ GenAI Travel Concierge Engine

An industry-grade GenAI microservice for **ConciergeIQ - AI Personal Travel Planner**, designed as a final year college engineering project. Built using Python, FastAPI, and Google Gemini API.

---

## 🛠️ Tech Stack & Architecture

- **Core Framework**: FastAPI, Python 3.12
- **GenAI Orchestrator**: LangChain, Google Gemini API (`gemini-1.5-flash`)
- **Semantic DB**: Custom Pure-Python TF-IDF Cosine Similarity Store (Fast & Zero-dependency)
- **Local Cache & Memory**: SQLite database storing user chat state.
- **External API Integrations**: Google Maps Directions/Places, OpenWeather, Foursquare.

### Microservice Folder Structure

```
GenAI/
├── app.py                     # Main application entry point
├── requirements.txt           # Python dependency declarations
├── .env                       # Environment credentials
├── routes/                    # API Endpoints
│   ├── chat.py                # Conversational AI planner
│   ├── itinerary.py           # Day plan timeline builder
│   ├── explore.py             # Sights browser
│   ├── recommendations.py     # Personalized sights ranking
│   └── health.py              # Diagnostics endpoint
├── agents/                    # Multi-agent AI workflow
│   ├── intent_agent.py        # Intent parser
│   ├── retriever_agent.py     # Sights filter
│   ├── weather_agent.py       # Weather constraints checker
│   ├── budget_agent.py        # Budget auditor
│   ├── planner_agent.py       # Itinerary scheduler
│   ├── validator_agent.py     # Overlap auditor
│   └── response_agent.py      # Output JSON formatter
├── services/                  # Business services
│   ├── maps.py                # Geocoding & ETA calculator
│   ├── weather.py             # Forecast retriever
│   ├── budget.py              # Spending checks
│   ├── recommendations.py     # Sights suggester
│   └── cache.py               # API request caching
└── README.md
```

---

## 🚀 Installation & Host Execution (No Docker)

### 1. Prerequisites
Ensure you have **Python 3.12** installed on your host machine.

### 2. Configure Environment
Create a copy of `.env.example` named `.env` and fill in your Gemini and Maps keys:
```env
GEMINI_API_KEY=your_gemini_key_here
GOOGLE_MAPS_API_KEY=your_maps_key_here
OPENWEATHER_API_KEY=your_weather_key_here
```

### 3. Setup Virtual Environment
Run the following in your terminal inside the `GenAI/` folder:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Concierge Engine
```cmd
python app.py
```
*The microservice will boot and run on `http://127.0.0.1:8085`.*

---

## 🔌 API Endpoints Documentation

- **POST `/api/chat`**: Process conversational travel queries statefully.
- **POST `/api/itinerary`**: Directly plan itineraries from a traveler profile object.
- **POST `/api/explore`**: Search hotels, temples, and sights.
- **GET `/api/health`**: Run diagnostics and check API connections.
- **Swagger Docs UI**: Open `http://127.0.0.1:8085/docs` in your browser.
