from datetime import datetime

from pydantic import BaseModel


class MemoOut(BaseModel):
    id: int
    content: str
    updated_at: datetime

    model_config = {"from_attributes": True}


class MemoUpdate(BaseModel):
    content: str
