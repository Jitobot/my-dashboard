from fastapi import APIRouter, HTTPException

from app.services.weather_service import CITIES, fetch_weather

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("")
async def get_weather(city: str = "tokyo"):
    city_info = CITIES.get(city)
    if not city_info:
        raise HTTPException(status_code=400, detail=f"Unknown city: {city}")
    data = await fetch_weather(city_info["lat"], city_info["lon"])
    data["city_name"] = city_info["name"]
    return data


@router.get("/cities")
def get_cities():
    return [{"id": k, "name": v["name"]} for k, v in CITIES.items()]
