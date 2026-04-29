from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.google_calendar import fetch_tasks, fetch_today_events, toggle_task

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


@router.get("/today")
def get_today_events():
    try:
        return fetch_today_events()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="credentials.json が見つかりません")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks")
def get_tasks():
    try:
        return fetch_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TaskToggle(BaseModel):
    tasklist_id: str
    task_id: str
    done: bool


@router.patch("/tasks")
def patch_task(data: TaskToggle):
    try:
        return toggle_task(data.tasklist_id, data.task_id, data.done)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
