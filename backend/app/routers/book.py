from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import BookCreate, BookRead, BookUpdate
from app.services import book_service

router = APIRouter(prefix="/book", tags=["Book"])

# 책 등록
@router.post("/", response_model=BookRead)
async def create(book: BookCreate, db: AsyncSession = Depends(get_async_db)):
    return await book_service.repository.create(db, obj_in=book)

# 등록된 책 전체 조회
@router.get("/", response_model=list[BookRead])
async def list(db: AsyncSession = Depends(get_async_db)):
    return await book_service.repository.get_all(db)

# 특정 책 조회
@router.get("/{book_id}", response_model=BookRead)
async def get(book_id: int, db: AsyncSession = Depends(get_async_db)):
    book = await book_service.repository.get(db, id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# 책 정보 수정
@router.put("/{book_id}", response_model=BookRead)
async def update(book_id: int, book_in: BookUpdate, db: AsyncSession = Depends(get_async_db)):
    book = await book_service.repository.get(db, id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book = await book_service.repository.update(db, db_obj=book, obj_in=book_in)
    return book

# 등록된 책 삭제
@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_async_db)):
    book = await book_service.repository.get(db, id=book_id)
    if not book:
        raise HTTPException(status_code=400, detail="책을 찾을 수 없습니다.")
    await book_service.repository.remove(db, id=book_id)
    return {"message": "책 삭제 됨"}