from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import DramaCreate, DramaRead, DramaUpdate
from app.services.drama import drama_service

router = APIRouter(prefix="/drama", tags=["Drama"])

@router.post("/", response_model=DramaRead)
async def create(drama: DramaCreate, db: AsyncSession = Depends(get_async_db)):
    return await drama_service.repository.create(db, obj_in=drama)

@router.get("/", response_model=list[DramaRead])
async def list(db: AsyncSession = Depends(get_async_db)):
    return await drama_service.repository.get_all(db)

@router.get("/{drama_id}", response_model=DramaRead)
async def get(drama_id: int, db: AsyncSession = Depends(get_async_db)):
    drama = await drama_service.repository.get(db, id=drama_id)
    if not drama:
        raise HTTPException(status_code=404, detail="Drama not found")
    return drama

@router.put("/{drama_id}", response_model=DramaRead)
async def update(drama_id: int, drama_in: DramaUpdate, db: AsyncSession = Depends(get_async_db)):
    drama = await drama_service.repository.get(db, id=drama_id)
    if not drama:
        raise HTTPException(status_code=404, detail="Drama not found")
    drama = await drama_service.repository.update(db, db_obj=drama, obj_in=drama_in)
    return drama

@router.delete("/{drama_id}")
async def delete(drama_id: int, db: AsyncSession = Depends(get_async_db)):
    drama = await drama_service.repository.get(db, id=drama_id)
    if not drama:
        raise HTTPException(status_code=400, detail="Drama not found")
    await drama_service.repository.remove(db, id=drama_id)
    return {"message": "Drama deleted"}
