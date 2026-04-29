import os
from datetime import datetime, timedelta, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/tasks",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def get_credentials() -> Credentials:
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8090)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


def fetch_today_events() -> list[dict]:
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_of_day.isoformat(),
            timeMax=end_of_day.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = []
    for item in result.get("items", []):
        start_raw = item["start"].get("dateTime", "")
        end_raw = item["end"].get("dateTime", "")
        if start_raw:
            start_dt = datetime.fromisoformat(start_raw).astimezone(jst)
            end_dt = datetime.fromisoformat(end_raw).astimezone(jst)
            time_str = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
        else:
            time_str = "終日"
        events.append({
            "summary": item.get("summary", "(タイトルなし)"),
            "time": time_str,
        })
    return events


def fetch_tasks() -> list[dict]:
    creds = get_credentials()
    service = build("tasks", "v1", credentials=creds)

    jst = timezone(timedelta(hours=9))
    today = datetime.now(jst).date()

    tasklists = service.tasklists().list(maxResults=10).execute()
    all_tasks = []

    for tasklist in tasklists.get("items", []):
        result = (
            service.tasks()
            .list(
                tasklist=tasklist["id"],
                showCompleted=True,
                showHidden=False,
                maxResults=50,
            )
            .execute()
        )
        for item in result.get("items", []):
            due = item.get("due", "")
            if not due:
                continue
            # due は "2026-02-24T00:00:00.000Z" 形式
            due_date = datetime.fromisoformat(due.replace("Z", "+00:00")).astimezone(jst).date()
            if due_date != today:
                continue
            all_tasks.append({
                "id": item["id"],
                "tasklist_id": tasklist["id"],
                "title": item.get("title", ""),
                "done": item.get("status") == "completed",
                "due": due,
                "list_name": tasklist.get("title", ""),
            })

    all_tasks.sort(key=lambda t: (t["done"], t["title"]))
    return all_tasks


def toggle_task(tasklist_id: str, task_id: str, done: bool) -> dict:
    creds = get_credentials()
    service = build("tasks", "v1", credentials=creds)

    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    task["status"] = "completed" if done else "needsAction"
    if not done:
        task.pop("completed", None)

    updated = service.tasks().update(
        tasklist=tasklist_id, task=task_id, body=task
    ).execute()
    return {
        "id": updated["id"],
        "done": updated.get("status") == "completed",
    }
