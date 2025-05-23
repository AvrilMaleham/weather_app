from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def weather():
    return {"message": "Weather"}

