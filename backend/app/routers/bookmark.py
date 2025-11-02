from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import BookmarkCreate, BookmarkRead
from app.services import bookmark_service
from app.models import Bookmark

router = APIRouter(prefix="/bookmark", tags=["Bookmark"])

# 북마크 추가
@router.post("/", response_model=BookmarkRead)
async def create_bookmark(bookmark: BookmarkCreate, db: AsyncSession = Depends(get_async_db)):
    return await bookmark_service.repository.create(db, obj_in=bookmark)

# 북마크 토글
@router.post("/toggle")
async def toggle_bookmark(bookmark_in: BookmarkCreate, db: AsyncSession = Depends(get_async_db)):
    bookmark = await bookmark_service.repository.get(db, id=(bookmark_in.user_id, bookmark_in.quote_id))
    if bookmark:
        await db.delete(bookmark)
        await db.commit()
        return {"bookmarked": False}
    else:
        new_bookmark = Bookmark(user_id=bookmark_in.user_id, quote_id=bookmark_in.quote_id)
        db.add(new_bookmark)
        await db.commit()
        return {"bookmarked": True}

# 조회
@router.get("/", response_model=list[BookmarkRead])
async def list_bookmark(db: AsyncSession = Depends(get_async_db)):
    return await bookmark_service.repository.get_all(db)

# 삭제
@router.delete("/")
async def delete_bookmark(user_id: int, quote_id: int, db: AsyncSession = Depends(get_async_db)):
    bookmark = await bookmark_service.repository.get(db, id=(user_id, quote_id)) # 복합키
    if not bookmark:
        raise HTTPException(status_code=400, detail="북마크를 찾을 수 없음")
    await bookmark_service.repository.remove(db, id=(user_id, quote_id))
    return {"message": "북마크 삭제 됨"}