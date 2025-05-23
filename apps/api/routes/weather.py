from fastapi import APIRouter
from services.weather_fetcher import fetch_and_store_weather

router = APIRouter()

@router.get("/")
def weather():
    return {"message": "Weather"}

