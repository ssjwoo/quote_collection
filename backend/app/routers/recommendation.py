from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import random

from app.database import get_async_db
from app.schemas import QuoteRead, UserResponse
from app.services import bookmark_service, quote_service
from app.routers.auth import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/user-based", response_model=List[QuoteRead])
async def get_user_based_recommendations(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get user-based recommended quotes.
    - If the user has bookmarks, it recommends quotes from the same source.
    - If the user has no bookmarks, it returns popular quotes.
    """
    # 1. Get user's bookmarks
    bookmarks = await bookmark_service.get_by_user_id(db, user_id=current_user.id)
    if not bookmarks:
        # If no bookmarks, return popular quotes
        return await quote_service.get_most_bookmarked(db, limit=10)

    # 2. Get source_ids from bookmarks
    source_ids = {bookmark.quote.source_id for bookmark in bookmarks}

    # 3. Get all quotes from those sources
    recommended_quotes = []
    for source_id in source_ids:
        quotes_from_source = await quote_service.repository.get_by_source_id(db, source_id=source_id)
        recommended_quotes.extend(quotes_from_source)

    # 4. Exclude already bookmarked quotes and user's own quotes
    bookmarked_quote_ids = {bookmark.quote_id for bookmark in bookmarks}
    final_recommendations = [
        quote for quote in recommended_quotes if quote.id not in bookmarked_quote_ids and quote.user_id != current_user.id
    ]
    
    # 5. if final_recommendations are more than 10, shuffle and return 10
    if len(final_recommendations) > 10:
        random.shuffle(final_recommendations)
        final_recommendations = final_recommendations[:10]

    return final_recommendations
