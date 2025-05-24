from fastapi import FastAPI
from routes import weather
from services.weather_fetcher import fetch_and_store_weather
from services.city_seeder import populate_cities
from contextlib import asynccontextmanager
from services.db import Base, engine

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Runs once when the app starts
    Base.metadata.create_all(bind=engine)
    populate_cities()
    await fetch_and_store_weather()
    yield
    # Runs once when the app shuts down (optional cleanup code can go here)

app = FastAPI(lifespan=lifespan)

@app.get("/")
def test():
    return {"hello": "world"}

app.include_router(weather.router, prefix="/weather", tags=["Weather"])

