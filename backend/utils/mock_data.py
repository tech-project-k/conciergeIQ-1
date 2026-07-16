import random

# Rich fallback mock database for travel planning when live APIs are disabled or credentials are missing
CITIES_DATABASE = {
    "paris": {
        "coords": {"lat": 48.8566, "lon": 2.3522},
        "hotels": [
            {
                "name": "Hotel Regina Louvre",
                "address": "2 Place des Pyramides, 75001 Paris, France",
                "phone": "+33 1 42 60 31 10",
                "website": "https://www.regina Louvre.com",
                "rating": 4.6,
                "cost_tier": "luxury",
                "price": 350.0,
                "coords": {"lat": 48.8631, "lon": 2.3323}
            },
            {
                "name": "Hotel Paris Lafayette",
                "address": "23 Rue de Messine, 75008 Paris, France",
                "phone": "+33 1 44 84 84 84",
                "website": "https://www.hotelparislafayette.com",
                "rating": 4.1,
                "cost_tier": "moderate",
                "price": 140.0,
                "coords": {"lat": 48.8778, "lon": 2.3178}
            },
            {
                "name": "Generator Paris Hostel",
                "address": "9-11 Place du Colonel Fabien, 75010 Paris, France",
                "phone": "+33 1 70 98 84 00",
                "website": "https://www.staygenerator.com/hostels/paris",
                "rating": 4.0,
                "cost_tier": "budget",
                "price": 45.0,
                "coords": {"lat": 48.8782, "lon": 2.3705}
            }
        ],
        "restaurants": [
            {
                "name": "Le Jules Verne",
                "type": "dinner",
                "address": "Eiffel Tower, 2nd Floor, 75007 Paris, France",
                "phone": "+33 1 45 55 61 44",
                "website": "https://www.lejulesverne.com",
                "rating": 4.7,
                "price": 180.0,
                "cost_tier": "luxury",
                "coords": {"lat": 48.8584, "lon": 2.2945},
                "tags": ["fine-dining", "french", "romantic"]
            },
            {
                "name": "Bouillon Chartier",
                "type": "lunch",
                "address": "7 Rue du Faubourg Montmartre, 75009 Paris, France",
                "phone": "+33 1 47 70 86 29",
                "website": "https://www.bouillon-chartier.com",
                "rating": 4.2,
                "price": 18.0,
                "cost_tier": "budget",
                "coords": {"lat": 48.8722, "lon": 2.3425},
                "tags": ["traditional", "french", "historic"]
            },
            {
                "name": "Angelina Paris",
                "type": "breakfast",
                "address": "226 Rue de Rivoli, 75001 Paris, France",
                "phone": "+33 1 42 60 82 00",
                "website": "https://www.angelina-paris.fr",
                "rating": 4.5,
                "price": 25.0,
                "cost_tier": "moderate",
                "coords": {"lat": 48.8626, "lon": 2.3283},
                "tags": ["pastries", "hot chocolate", "cafe"]
            },
            {
                "name": "L'As du Fallafel",
                "type": "lunch",
                "address": "34 Rue des Rosiers, 75004 Paris, France",
                "phone": "+33 1 48 87 63 60",
                "website": "https://lasdufallafel.com",
                "rating": 4.6,
                "price": 12.0,
                "cost_tier": "budget",
                "coords": {"lat": 48.8574, "lon": 2.3592},
                "tags": ["vegetarian", "street-food", "middle-eastern"]
            }
        ],
        "attractions": [
            {
                "name": "Eiffel Tower",
                "type": "attraction",
                "address": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France",
                "phone": "+33 892 70 12 39",
                "website": "https://www.toureiffel.paris",
                "rating": 4.7,
                "price": 26.80,
                "coords": {"lat": 48.8584, "lon": 2.2945},
                "hours": "09:00 - 23:45",
                "description": "Iconic 19th-century iron landmark tower designed by Gustave Eiffel with observation platforms."
            },
            {
                "name": "Louvre Museum",
                "type": "museum",
                "address": "Rue de Rivoli, 75001 Paris, France",
                "phone": "+33 1 40 20 53 17",
                "website": "https://www.louvre.fr",
                "rating": 4.7,
                "price": 17.00,
                "coords": {"lat": 48.8606, "lon": 2.3376},
                "hours": "09:00 - 18:00",
                "description": "World-famous art museum housing thousands of works, including the Mona Lisa and the Venus de Milo."
            },
            {
                "name": "Palais Garnier",
                "type": "attraction",
                "address": "Pl. de l'Opéra, 75009 Paris, France",
                "phone": "+33 1 71 25 24 23",
                "website": "https://www.operadeparis.fr",
                "rating": 4.8,
                "price": 14.00,
                "coords": {"lat": 48.8719, "lon": 2.3316},
                "hours": "10:00 - 17:00",
                "description": "Opulent 19th-century opera house which was the setting for the novel 'The Phantom of the Opera'."
            },
            {
                "name": "Jardin du Luxembourg",
                "type": "park",
                "address": "75006 Paris, France",
                "phone": "+33 1 42 34 20 00",
                "website": "https://www.senat.fr/visite/jardin/index.html",
                "rating": 4.7,
                "price": 0.0,
                "coords": {"lat": 48.8462, "lon": 2.3371},
                "hours": "07:30 - 21:30",
                "description": "17th-century park with formal lawns, fountains, statues and model sailboat basins."
            }
        ]
    },
    "tokyo": {
        "coords": {"lat": 35.6762, "lon": 139.6503},
        "hotels": [
            {
                "name": "Aman Tokyo",
                "address": "1-5-6 Otemachi, Chiyoda-ku, Tokyo, Japan",
                "phone": "+81 3-5224-3333",
                "website": "https://www.aman.com/resorts/aman-tokyo",
                "rating": 4.8,
                "cost_tier": "luxury",
                "price": 950.0,
                "coords": {"lat": 35.6848, "lon": 139.7645}
            },
            {
                "name": "Shibuya Stream Excel Hotel Tokyu",
                "address": "3-21-3 Shibuya, Shibuya-ku, Tokyo, Japan",
                "phone": "+81 3-5457-0109",
                "website": "https://www.tokyuhotelsjapan.com/shibuya-stream-e",
                "rating": 4.4,
                "cost_tier": "moderate",
                "price": 220.0,
                "coords": {"lat": 35.6565, "lon": 139.7032}
            },
            {
                "name": "Nine Hours Shinjuku-North",
                "address": "1-4-15 Hyakunincho, Shinjuku-ku, Tokyo, Japan",
                "phone": "+81 3-5291-7330",
                "website": "https://ninehours.co.jp/shinjuku-north",
                "rating": 4.0,
                "cost_tier": "budget",
                "price": 40.0,
                "coords": {"lat": 35.7011, "lon": 139.7021}
            }
        ],
        "restaurants": [
            {
                "name": "Sukiyabashi Jiro",
                "type": "dinner",
                "address": "4-2-15 Ginza, Chuo-ku, Tokyo, Japan",
                "phone": "+81 3-3535-3600",
                "website": "http://www.sushi-jiro.jp",
                "rating": 4.8,
                "price": 400.0,
                "cost_tier": "luxury",
                "coords": {"lat": 35.6723, "lon": 139.7634},
                "tags": ["sushi", "michelin", "world-famous"]
            },
            {
                "name": "Ichiran Shinjuku",
                "type": "lunch",
                "address": "3-34-11 Shinjuku, Tokyo, Japan",
                "phone": "+81 3-3225-5518",
                "website": "https://ichiran.com",
                "rating": 4.3,
                "price": 15.0,
                "cost_tier": "budget",
                "coords": {"lat": 35.6904, "lon": 139.7023},
                "tags": ["ramen", "tonkotsu", "quick-eat"]
            },
            {
                "name": "Tsukiji Outer Market Cafe",
                "type": "breakfast",
                "address": "4-16-2 Tsukiji, Chuo-ku, Tokyo, Japan",
                "phone": "+81 3-3541-9444",
                "website": "https://www.tsukiji.or.jp",
                "rating": 4.5,
                "price": 20.0,
                "cost_tier": "moderate",
                "coords": {"lat": 35.6655, "lon": 139.7702},
                "tags": ["seafood", "breakfast", "street-food"]
            }
        ],
        "attractions": [
            {
                "name": "Sensō-ji Temple",
                "type": "attraction",
                "address": "2-3-1 Asakusa, Taito-ku, Tokyo, Japan",
                "phone": "+81 3-3842-0181",
                "website": "https://www.senso-ji.jp",
                "rating": 4.6,
                "price": 0.0,
                "coords": {"lat": 35.7148, "lon": 139.7967},
                "hours": "06:00 - 17:00",
                "description": "Tokyo's oldest and most iconic Buddhist temple completed in 645 AD, dedicated to Bodhisattva Kannon."
            },
            {
                "name": "Shinjuku Gyoen National Garden",
                "type": "park",
                "address": "11 Naitomachi, Shinjuku-ku, Tokyo, Japan",
                "phone": "+81 3-3350-0151",
                "website": "https://www.env.go.jp/garden/shinjukugyoen",
                "rating": 4.7,
                "price": 4.0,
                "coords": {"lat": 35.6852, "lon": 139.7101},
                "hours": "09:00 - 16:30",
                "description": "A spacious garden combining Japanese Traditional, English Landscape, and French Formal styling."
            },
            {
                "name": "teamLab Planets",
                "type": "museum",
                "address": "6-1-16 Toyosu, Koto-ku, Tokyo, Japan",
                "phone": "+81 3-6273-0300",
                "website": "https://planets.teamlab.art/tokyo",
                "rating": 4.8,
                "price": 25.0,
                "coords": {"lat": 35.6491, "lon": 139.7898},
                "hours": "09:00 - 22:00",
                "description": "An immersive digital museum where visitors walk through water and interact with colorful, morphing projection art."
            }
        ]
    }
}

# Add default items for other cities dynamically
DEFAULT_CITY_PROFILE = {
    "coords": {"lat": 0.0, "lon": 0.0},
    "hotels": [
        {
            "name": "Grand Central Hotel",
            "address": "100 Main Street, City Center",
            "phone": "+1 555-0199",
            "website": "https://www.grandcentralhotel.com",
            "rating": 4.5,
            "cost_tier": "moderate",
            "price": 150.0,
            "coords": {"lat": 0.0, "lon": 0.0}
        }
    ],
    "restaurants": [
        {
            "name": "Central Bistro",
            "type": "lunch",
            "address": "15 Main Street, City Center",
            "phone": "+1 555-0240",
            "website": "https://www.centralbistro.com",
            "rating": 4.2,
            "price": 20.0,
            "cost_tier": "moderate",
            "coords": {"lat": 0.001, "lon": 0.001},
            "tags": ["local", "bistro"]
        }
    ],
    "attractions": [
        {
            "name": "City Museum of Art",
            "type": "museum",
            "address": "50 Culture Blvd",
            "phone": "+1 555-0301",
            "website": "https://www.cityartmuseum.org",
            "rating": 4.6,
            "price": 10.0,
            "coords": {"lat": -0.001, "lon": -0.001},
            "hours": "09:00 - 17:00",
            "description": "Featuring classic and contemporary regional masterpieces."
        }
    ]
}

def get_fallback_data(city: str) -> dict:
    cleaned = city.lower().strip()
    if cleaned in CITIES_DATABASE:
        return CITIES_DATABASE[cleaned]
    
    # Generate realistic values for unknown cities
    # Start with simple latitude/longitude based on random generation around a dummy point, or return DEFAULT_CITY_PROFILE
    prof = DEFAULT_CITY_PROFILE.copy()
    # Populate with city specific titles
    prof["hotels"][0]["name"] = f"Luxury Inn {city.capitalize()}"
    prof["restaurants"][0]["name"] = f"Gourmet {city.capitalize()} Kitchen"
    prof["attractions"][0]["name"] = f"Central {city.capitalize()} Square"
    return prof
