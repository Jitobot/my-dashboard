from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Memo
from app.schemas import MemoOut, MemoUpdate

router = APIRouter(prefix="/api/memo", tags=["memo"])


@router.get("", response_model=MemoOut)
def get_memo(db: Session = Depends(get_db)):
    memo = db.query(Memo).first()
    if not memo:
        memo = Memo(content="")
        db.add(memo)
        db.commit()
        db.refresh(memo)
    return memo


@router.put("", response_model=MemoOut)
def update_memo(data: MemoUpdate, db: Session = Depends(get_db)):
    memo = db.query(Memo).first()
    if not memo:
        memo = Memo(content=data.content, updated_at=datetime.now(timezone.utc))
        db.add(memo)
    else:
        memo.content = data.content
        memo.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(memo)
    return memo
