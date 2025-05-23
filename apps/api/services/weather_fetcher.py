import requests
from datetime import datetime, timedelta
from .db import SessionLocal, engine
from .models import Base, Weather

API_KEY = "1046fa4e5a634f7e998191145252305"
CITIES = ["Auckland", "Sydney", "New York", "London"]

Base.metadata.create_all(bind=engine)

def fetch_and_store_weather():
    session = SessionLocal()
    try:
        for city in CITIES:
            for i in range(7):
                date = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
                url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city}&dt={date}"
                response = requests.get(url)
                data = response.json()
                day = data['forecast']['forecastday'][0]['day']
                condition = day['condition']['text']

                weather = Weather(
                    city=city,
                    date=date,
                    maxtemp_c=day['maxtemp_c'],
                    mintemp_c=day['mintemp_c'],
                    avgtemp_c=day['avgtemp_c'],
                    condition_text=condition
                )
                session.add(weather)
        session.commit()
    finally:
        session.close()
