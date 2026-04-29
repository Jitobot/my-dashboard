from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Bookmark
from app.schemas import BookmarkCreate, BookmarkOut

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])


@router.get("", response_model=list[BookmarkOut])
def get_bookmarks(db: Session = Depends(get_db)):
    return db.query(Bookmark).order_by(Bookmark.position).all()


@router.post("", response_model=BookmarkOut)
def create_bookmark(data: BookmarkCreate, db: Session = Depends(get_db)):
    max_pos = db.query(Bookmark.position).order_by(Bookmark.position.desc()).first()
    position = (max_pos[0] + 1) if max_pos else 0
    bookmark = Bookmark(
        title=data.title, url=data.url, icon=data.icon, position=position
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


@router.delete("/{bookmark_id}")
def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)):
    bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if bookmark:
        db.delete(bookmark)
        db.commit()
    return {"ok": True}
