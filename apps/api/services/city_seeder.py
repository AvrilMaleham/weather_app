from .db import SessionLocal
from .models import City

def populate_cities():
    session = SessionLocal()
    try:
        cities = [
        {"name": "Auckland", "country": "New Zealand", "latitude": -36.8485, "longitude": 174.7633},
        {"name": "Sydney", "country": "Australia", "latitude": -33.8688, "longitude": 151.2093},
        {"name": "London", "country": "UK", "latitude": 51.5074, "longitude": -0.1278},
        {"name": "Los Angeles", "country": "USA", "latitude": 34.0522, "longitude": -118.2437},
        {"name": "Bengaluru", "country": "India", "latitude": 12.9716, "longitude": 77.5946},
    ]

        for city in cities:
            existing = session.query(City).filter_by(name=city["name"]).first()
            if not existing:
                session.add(City(**city))

        session.commit()
    finally:
        session.close()
