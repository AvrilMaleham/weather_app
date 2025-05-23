from fastapi import FastAPI
from routes import weather
from services.weather_fetcher import fetch_and_store_weather
from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(_app: FastAPI):
#     # Runs once when the app starts
#     await fetch_and_store_weather()  # Added 'await' here
#     yield
#     # Runs once when the app shuts down (optional cleanup code can go here)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("🌟 App is starting up!")  # This will show in the Docker or terminal logs
    yield
    print("👋 App is shutting down!")  # This runs on shutdown

app = FastAPI(lifespan=lifespan)

@app.get("/")
def test():
    return {"hello": "world"}

app.include_router(weather.router, prefix="/weather", tags=["Weather"])

