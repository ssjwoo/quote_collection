from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import random

from app.database import get_async_db
from app.schemas import QuoteRead, UserResponse
from app.services import bookmark_service, quote_service
from app.routers.auth import get_current_user
from app.core.config import settings
import sys
import os

# Add llm folder to sys.path to import AIService
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../llm")))

try:
    from ai_service import AIService
except ImportError as e:
    # Fallback or error handling if path is wrong
    with open("import_error.log", "a", encoding="utf-8") as f:
        import traceback
        f.write(f"ImportError in recommendation.py: {e}\n")
        f.write(traceback.format_exc())
    print("Could not import AIService from llm folder")
    AIService = None

from fastapi.security import OAuth2PasswordBearer
from app.core.auth import verify_token
from app.services import user_service

# Optional auth scheme
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

async def get_current_user_optional(
    token: str = Depends(oauth2_scheme_optional),
    db: AsyncSession = Depends(get_async_db)
):
    if not token:
        return None
    try:
        user_id = verify_token(token)
        user = await user_service.repository.get(db, id=user_id)
        return user
    except Exception:
        return None

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

# Initialize AIService globally or lazily
# We pass settings here
# Initialize AIService globally or lazily
# We pass settings here
ai_service = AIService(
    project_id=settings.google_project_id, 
    location="us-central1", # Force us-central1
    aladin_api_key=settings.aladin_api_key
) if AIService else None


from app.services.ai_recommendation_service import AIRecommendationService

# Initialize Service
ai_rec_service = AIRecommendationService(ai_service)

@router.get("/", response_model=List[QuoteRead])
async def get_recommendations_by_source(
    db: AsyncSession = Depends(get_async_db),
    source_type: str = Query("book", enum=["book"]),
    limit: int = 3,
    current_user: UserResponse = Depends(get_current_user_optional),
):
    """Get recommended quotes from AI/DB with variety."""
    user_id = current_user.id if current_user else None
    return await ai_rec_service.get_quotes_recommendations(db, source_type, limit, user_id)

@router.post("/related", response_model=List[QuoteRead])
async def get_related_recommendations(
    current_quote_content: str = Body(..., embed=True),
    limit: int = 3,
):
    """Chain Recommendation for Detail page."""
    return await ai_rec_service.get_related_chain(current_quote_content, limit)

@router.get("/user-based", response_model=List[QuoteRead])
async def get_user_based_recommendations(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserResponse = Depends(get_current_user),
):
    # This logic is purely DB-based, fits in a normal service but keeping here for now as it's not and LLM one.
    # Refactoring purely DB logic to services/bookmark_service in next step if needed.
    bookmarks = await bookmark_service.get_by_user_id(db, user_id=current_user.id)
    if not bookmarks:
        return await quote_service.get_most_bookmarked(db, limit=10)

    source_ids = {bookmark.quote.source_id for bookmark in bookmarks}
    recommended_quotes = []
    for source_id in source_ids:
        quotes_from_source = await quote_service.repository.get_by_source_id(db, source_id=source_id)
        recommended_quotes.extend(quotes_from_source)

    bookmarked_quote_ids = {bookmark.quote_id for bookmark in bookmarks}
    final = [q for q in recommended_quotes if q.id not in bookmarked_quote_ids and q.user_id != current_user.id]
    
    if len(final) > 10:
        random.shuffle(final)
        final = final[:10]
    return final

from app.schemas.recommendation import BookRecommendation

@router.post("/ai", response_model=List[BookRecommendation])
async def get_ai_recommendations(
    refresh: bool = Query(False),
    db: AsyncSession = Depends(get_async_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """Get AI book recommendations."""
    if not ai_service: return []
    user_context = await ai_rec_service.get_user_context(db, current_user.id)
    return await ai_service.generate_book_recommendations(user_context, bypass_cache=refresh)
