from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import logging
from sqlalchemy.future import select

from app.database import get_async_db
from app.schemas import PublisherCreate, PublisherRead, PublisherUpdate, ProducerCreate, ProducerRead, ProducerUpdate
from app.services import publisher_service, producer_service
from app.models import Producer

router = APIRouter(prefix="/producers", tags=["Producers"])

logger = logging.getLogger(__name__)

# 프로듀서 등록
@router.post("/", response_model=ProducerRead)
async def create_producer(producer: ProducerCreate, db: AsyncSession = Depends(get_async_db)):
    existing_producer = await producer_service.repository.get_by_name(db, name=producer.name)
    if existing_producer:
        return existing_producer
    try:
        new_producer = await producer_service.repository.create(db, obj_in=producer)
        producer_id = new_producer.id # Get ID before commit
        await db.commit()
        
        # Fetch a fresh object from the database to ensure it's fully loaded
        result = await db.execute(select(Producer).where(Producer.id == producer_id))
        final_producer = result.scalar_one()
        return final_producer
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Producer with this name already exists")
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating producer: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")

# 등록된 프로듀서 전체 조회
@router.get("/", response_model=list[ProducerRead])
async def list_producers(db: AsyncSession = Depends(get_async_db)):
    return await producer_service.repository.get_all(db)

# 특정 프로듀서 조회
@router.get("/{producer_id}", response_model=ProducerRead)
async def get_producer(producer_id: int, db: AsyncSession = Depends(get_async_db)):
    producer = await producer_service.repository.get(db, id=producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer

# 프로듀서 정보 수정
@router.put("/{producer_id}", response_model=ProducerRead)
async def update_producer(
    producer_id: int, producer_in: ProducerUpdate, db: AsyncSession = Depends(get_async_db)
):
    producer = await producer_service.repository.get(db, id=producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    producer = await producer_service.repository.update(db, db_obj=producer, obj_in=producer_in)
    return producer

# 등록된 프로듀서 삭제
@router.delete("/{producer_id}")
async def delete_producer(producer_id: int, db: AsyncSession = Depends(get_async_db)):
    producer = await producer_service.repository.get(db, id=producer_id)
    if not producer:
        raise HTTPException(status_code=400, detail="프로듀서를 찾을 수 없습니다.")
    await producer_service.repository.remove(db, id=producer_id)
    return {"message": "프로듀서 삭제 됨"}
