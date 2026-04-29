from fastapi import APIRouter, HTTPException

from app.services.news_service import fetch_news

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("")
async def get_news():
    try:
        return await fetch_news()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
