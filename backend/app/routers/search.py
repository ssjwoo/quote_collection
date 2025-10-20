from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.schemas import SearchResult
from app.services.search import search_service

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=SearchResult)
async def search(q: str = Query(..., min_length=1), db: AsyncSession = Depends(get_async_db)):
    return await search_service.search(db, query=q)
