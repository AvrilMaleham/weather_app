import httpx
from .db import SessionLocal
from .models import City, WeatherHistory
from datetime import datetime, timedelta

CITY_COORDS = {
    "Auckland": (-36.8485, 174.7633),
    "Sydney": (-33.8688, 151.2093),
    "London": (51.5074, -0.1278),
    "Los Angeles": (34.0522, -118.2437),
    "Bengaluru": (12.9716, 77.5946),
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
            for city_name in CITY_COORDS.keys():
                city = session.query(City).filter_by(name=city_name).first()
                if not city:
                    city = City(name=city_name)
                    session.add(city)
            session.commit()

            for city_name, (lat, lon) in CITY_COORDS.items():
                city = session.query(City).filter_by(name=city_name).first()

                url = (
                    f"https://archive-api.open-meteo.com/v1/archive?"
                    f"latitude={lat}&longitude={lon}&start_date={start_date}"
                    f"&end_date={end_date}"
                    f"&daily=temperature_2m_mean,windspeed_10m_max,precipitation_sum"
                    f"&timezone=auto"
                )

                response = await client.get(url)
                data = response.json()

                dates = data["daily"]["time"]
                temps_c = data["daily"]["temperature_2m_mean"]
                wind_kph = data["daily"]["windspeed_10m_max"]
                precip_mm = data["daily"]["precipitation_sum"]

                for date, temp_c, wind_k, precip_m in zip(dates, temps_c, wind_kph, precip_mm):
                    date_obj = datetime.strptime(date, "%Y-%m-%d").date()

                    weather = WeatherHistory(
                        city_id=city.id,
                        avgtemp_c=round(temp_c, 1),
                        avgtemp_f=round((temp_c * 9 / 5) + 32, 1),
                        maxwind_kph=round(wind_k, 1),
                        maxwind_mph=round(wind_k * 0.621371, 1),
                        totalprecip_mm=round(precip_m, 2),
                        totalprecip_in=round(precip_m / 25.4, 2),
                        date=date_obj,
                    )
                    session.add(weather)

            session.commit()
        finally:
            session.close()
