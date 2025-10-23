from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_async_db
from app.schemas import (
    UserResponse,
    UserUpdate,
    UserCheckName,
    CheckNameResponse,
    QuoteRead,
)
from app.services import user_service, quote_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/check-name", response_model=CheckNameResponse)
async def check_user_name(
    user_check: UserCheckName, db: AsyncSession = Depends(get_async_db)
):
    user = await user_service.repository.get_by_username(db, username=user_check.username)
    return CheckNameResponse(is_available=user is None)


@router.get("/", response_model=List[UserResponse])
async def list_users(db: AsyncSession = Depends(get_async_db)):
    return await user_service.repository.get_all(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await user_service.repository.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_async_db)):
    user = await user_service.repository.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await user_service.repository.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await user_service.repository.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_service.repository.remove(db, id=user_id)
    return {"message": "User deleted successfully"}


@router.get("/{user_id}/quotes", response_model=List[QuoteRead])
async def get_user_quotes(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await user_service.repository.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await quote_service.get_by_user_id(db, user_id=user_id)
