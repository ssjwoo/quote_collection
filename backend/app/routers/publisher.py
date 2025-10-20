from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import PublisherCreate, PublisherRead, PublisherUpdate
from app.services import publisher_service

router = APIRouter(prefix="/publisher", tags=["Publisher"])

# 출판사 등록
@router.post("/", response_model=PublisherRead)
async def create(publisher: PublisherCreate, db: AsyncSession = Depends(get_async_db)):
    return await publisher_service.repository.create(db, obj_in=publisher)

# 등록된 출판사 전체 조회
@router.get("/", response_model=list[PublisherRead])
async def list(db: AsyncSession = Depends(get_async_db)):
    return await publisher_service.repository.get_all(db)

# 특정 출판사 조회
@router.get("/{publisher_id}", response_model=PublisherRead)
async def get(publisher_id: int, db: AsyncSession = Depends(get_async_db)):
    publisher = await publisher_service.repository.get(db, id=publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher

# 출판사 정보 수정
@router.put("/{publisher_id}", response_model=PublisherRead)
async def update(publisher_id: int, publisher_in: PublisherUpdate, db: AsyncSession = Depends(get_async_db)):
    publisher = await publisher_service.repository.get(db, id=publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    publisher = await publisher_service.repository.update(db, db_obj=publisher, obj_in=publisher_in)
    return publisher

# 등록된 출판사 삭제
@router.delete("/{publisher_id}")
async def delete_publisher(publisher_id: int, db: AsyncSession = Depends(get_async_db)):
    publisher = await publisher_service.repository.get(db, id=publisher_id)
    if not publisher:
        raise HTTPException(status_code=400, detail="출판사를 찾을 수 없습니다.")
    await publisher_service.repository.remove(db, id=publisher_id)
    return {"message": "출판사 삭제 됨"}