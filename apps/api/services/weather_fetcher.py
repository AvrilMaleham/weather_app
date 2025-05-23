import httpx
from .db import SessionLocal
from .models import Weather
from datetime import datetime, timedelta

CITY_COORDS = {
    "Auckland": (-36.8485, 174.7633),
    "Sydney": (-33.8688, 151.2093),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
}

def get_most_recent_7_days():
    today = datetime.today()
    end_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    start_date = (today - timedelta(days=14)).strftime('%Y-%m-%d')
    return start_date, end_date
    

async def fetch_and_store_weather():
    session = SessionLocal()
    start_date, end_date = get_most_recent_7_days()

    async with httpx.AsyncClient() as client:
        try:
            for city, (lat, lon) in CITY_COORDS.items():
                url = (
                    f"https://archive-api.open-meteo.com/v1/archive?"
                    f"latitude={lat}&longitude={lon}&start_date={start_date}"
                    f"&end_date={end_date}&daily=temperature_2m_mean&timezone=auto"
                )
                response = await client.get(url)
                data = response.json()

                for date, avgtemp in zip(data["daily"]["time"], data["daily"]["temperature_2m_mean"]):
                    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                    weather = Weather(
                        city=city,
                        date=date_obj,
                        avgtemp_c=avgtemp,
                    )
                    session.add(weather)

            session.commit()
        finally:
            session.close()
