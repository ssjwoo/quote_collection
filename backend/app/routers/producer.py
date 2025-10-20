from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import ProducerCreate, ProducerRead, ProducerUpdate
from app.services import producer_service

router = APIRouter(prefix="/producers", tags=["Producers"])

# 제작사 등록
@router.post("/", response_model=ProducerRead)
async def create_producer(producer: ProducerCreate, db: AsyncSession = Depends(get_async_db)):
    return await producer_service.repository.create(db, obj_in=producer)

# 등록된 제작사 전체 조회
@router.get("/", response_model=list[ProducerRead])
async def list_producers(db: AsyncSession = Depends(get_async_db)):
    return await producer_service.repository.get_all(db)

# 특정 제작사 조회
@router.get("/{producer_id}", response_model=ProducerRead)
async def get_producer(producer_id: int, db: AsyncSession = Depends(get_async_db)):
    producer = await producer_service.repository.get(db, id=producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer

# 제작사 정보 수정
@router.put("/{producer_id}", response_model=ProducerRead)
async def update_producer(producer_id: int, producer_in: ProducerUpdate, db: AsyncSession = Depends(get_async_db)):
    producer = await producer_service.repository.get(db, id=producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    producer = await producer_service.repository.update(db, db_obj=producer, obj_in=producer_in)
    return producer

# 등록된 제작사 삭제
@router.delete("/{producer_id}")
async def delete_producer(producer_id: int, db: AsyncSession = Depends(get_async_db)):
    producer = await producer_service.repository.get(db, id=producer_id)
    if not producer:
        raise HTTPException(status_code=400, detail="제작사를 찾을 수 없습니다.")
    await producer_service.repository.remove(db, id=producer_id)
    return {"message": "제작사 삭제 완료"}
