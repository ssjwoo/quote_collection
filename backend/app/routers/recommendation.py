from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_async_db
from app.models import Quote, Bookmark
from app.schemas.quote import QuoteRead         
from app.schemas.user import UserResponse        
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/", response_model=List[QuoteRead])
async def user_based_recommendations(
    db: AsyncSession = Depends(get_async_db),
    me: UserResponse = Depends(get_current_user),
):
    result = await db.execute(
        select(Bookmark.quote_id).where(Bookmark.user_id == me.id)
    )
    bookmarked_ids = set(result.scalars().all())

    if not bookmarked_ids:
        return []

    result = await db.execute(
        select(Quote.source_id).where(Quote.id.in_(bookmarked_ids))
    )
    source_ids = set(result.scalars().all())
    if not source_ids:
        return []

    result = await db.execute(
        select(Quote).where(Quote.source_id.in_(source_ids))
    )
    quotes = list(result.scalars().all())
    return quotes[:5]