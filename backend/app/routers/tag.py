from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import TagCreate, TagRead, TagUpdate
from app.services import tag_service

router = APIRouter(prefix="/tag", tags=["Tag"])

# 새 태그 생성
@router.post("/", response_model=TagRead)
async def create(tag: TagCreate, db: AsyncSession = Depends(get_async_db)):
    return await tag_service.repository.create(db, obj_in=tag)

# 태그 전체 조회
@router.get("/", response_model=list[TagRead])
async def list(db: AsyncSession = Depends(get_async_db)):
    return await tag_service.repository.get_all(db)

# 특정 태그 조회
@router.get("/{tag_id}", response_model=TagRead)
async def get(tag_id: int, db: AsyncSession = Depends(get_async_db)):
    tag = await tag_service.repository.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

# 태그 정보 수정
@router.put("/{tag_id}", response_model=TagRead)
async def update(tag_id: int, tag_in: TagUpdate, db: AsyncSession = Depends(get_async_db)):
    tag = await tag_service.repository.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = await tag_service.repository.update(db, db_obj=tag, obj_in=tag_in)
    return tag

# 태그 삭제
@router.delete("/{tag_id}")
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_async_db)):
    tag = await tag_service.repository.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=400, detail="태그를 찾을 수 없습니다.")
    await tag_service.repository.remove(db, id=tag_id)
    return {"message": "태그 삭제 됨"}