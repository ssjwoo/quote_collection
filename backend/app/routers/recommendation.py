from fastapi import APIRouter, Depends, Query
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
# Assuming backend is running from c:\quote_collection\backend
# We need to go up one level to c:\quote_collection, then into llm
# However, inside the container or runtime, we must validata the path.
# __file__ is .../backend/app/routers/recommendation.py
# ../../../llm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../llm")))

try:
    from ai_service import AIService
except ImportError:
    # Fallback or error handling if path is wrong
    print("Could not import AIService from llm folder")
    AIService = None

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

# Initialize AIService globally or lazily
# We pass settings here
print(f"DEBUG RECOM: Initializing AIService with Aladin Key: {settings.aladin_api_key[:5]}***")
ai_service = AIService(
    project_id=settings.google_project_id, 
    location=settings.google_location,
    aladin_api_key=settings.aladin_api_key
) if AIService else None


@router.get("/", response_model=List[QuoteRead])
async def get_recommendations_by_source(
    db: AsyncSession = Depends(get_async_db),
    source_type: str = Query("book", enum=["book", "movie", "drama"]),
    limit: int = 3,
):
    """
    Get recommended quotes from a specific source type.
    """
    # quotes = await quote_service.get_random_by_source_type(
    #     db, source_type=source_type, limit=limit
    # )

    # if quotes:
    #     return quotes

    # Fallback to AI if no quotes found in DB
    if ai_service:
        ai_quotes = await ai_service.get_recommendations(source_type, limit)
        if ai_quotes:
            from app.schemas.source import SourceRead
            from app.schemas.tag import TagRead
            from datetime import datetime
            
            recommendations = []
            for i, q in enumerate(ai_quotes):
                # Using negative ID to indicate it's not a real DB record
                fake_id = -1 * (i + 1)
                
                # Process tags
                tags_data = q.get("tags", [])
                tags_list = []
                if isinstance(tags_data, list):
                    for t_idx, t_name in enumerate(tags_data):
                        tags_list.append(TagRead(
                            id=-1 * (t_idx + 1),
                            name=str(t_name),
                            created_at=datetime.now()
                        ))
                
                # Construct dummy source
                source_read = SourceRead(
                    id=0,
                    title=q.get("source_title", "Unknown Source"),
                    source_type=source_type,
                    creator=q.get("author", "Unknown Author"),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                # Construct dummy quote
                quote_read = QuoteRead(
                    id=fake_id, 
                    content=q.get('content', ''),
                    source_id=0,
                    user_id=0,
                    created_at=datetime.now(),
                    tags=tags_list,
                    source=source_read
                )
                recommendations.append(quote_read)
            return recommendations
            
    return []


@router.get("/user-based", response_model=List[QuoteRead])
async def get_user_based_recommendations(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserResponse = Depends(get_current_user),
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


@router.post("/ai", response_model=str)
async def get_ai_recommendations(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Get AI-based book recommendations using Vertex AI (Gemini).
    It calls the AI service with the user's recent bookmarks and quotes as context.
    """
    if not ai_service:
        return "AI 서비스가 서버에서 활성화되지 않았습니다."
    
    # 1. Gather User Context: Recent Bookmarks and Quotes
    # Get recent bookmarks
    bookmarks = await bookmark_service.get_by_user_id(db, user_id=current_user.id)
    
    # Get user's own quotes
    user_quotes = await quote_service.get_by_user_id(db, user_id=current_user.id)

    context_lines = []
    
    # Summarize Bookmarks
    if bookmarks:
        context_lines.append("--- User's Bookmarks ---")
        for b in bookmarks[:10]: # Limit to last 10
            q = b.quote
            source_title = q.source.title if q.source else "Unknown Source"
            context_lines.append(f"Source: {source_title}, Content: {q.content[:100]}...")
    
    # Summarize User's Quotes
    if user_quotes:
        context_lines.append("--- User's Quotes ---")
        for q in user_quotes[:10]: # Limit to last 10
             source_title = q.source.title if q.source else "Unknown Source"
             context_lines.append(f"Source: {source_title}, Content: {q.content[:100]}...")

    user_context = "\n".join(context_lines)
    
    # 2. Call AI Service
    recommendations = await ai_service.generate_book_recommendations(user_context)
    
    return recommendations
