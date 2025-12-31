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


@router.get("/", response_model=List[QuoteRead])
async def get_recommendations_by_source(
    db: AsyncSession = Depends(get_async_db),
    source_type: str = Query("book", enum=["book", "movie", "drama"]),
    limit: int = 3,
    current_user: UserResponse = Depends(get_current_user_optional),
):
    """
    Get recommended quotes from a specific source type.
    Personalized if user is logged in.
    """
    # 1. Build User Context if logged in
    user_context = ""
    if current_user:
        try:
            # Fetch bookmarks
            bookmarks = await bookmark_service.get_by_user_id(db, user_id=current_user.id)
            # Fetch user's own quotes
            user_quotes = await quote_service.get_by_user_id(db, user_id=current_user.id)
            
            context_parts = []
            if bookmarks:
                context_parts.append("User Bookmarks provided below:")
                for b in bookmarks[:5]: # Use top 5 recent bookmarks
                    try:
                        q = b.quote
                        # Explicitly access attributes to ensure they are loaded (if lazy)
                        # Depending on schema, might need to ensure eager loading or access carefully
                        content = q.content[:50] if q.content else ""
                        tags = ",".join([t.name for t in q.tags]) if q.tags else ""
                        context_parts.append(f"- Quote: {content} (Tags: {tags})")
                    except Exception as e:
                        print(f"Error processing bookmark for context: {e}")
                        continue
            
            if user_quotes:
                context_parts.append("User Created Quotes:")
                for q in user_quotes[:5]:
                    try:
                        content = q.content[:50] if q.content else ""
                        tags = ",".join([t.name for t in q.tags]) if q.tags else ""
                        context_parts.append(f"- Quote: {content} (Tags: {tags})")
                    except Exception as e:
                        print(f"Error processing user quote for context: {e}")
                        continue
            
            if context_parts:
                user_context = "\n".join(context_parts)
                print(f"DEBUG: Recommendation logic using context for user {current_user.id}: {len(user_context)} chars")
        except Exception as e:
            print(f"DEBUG: Failed to build user context: {e}")
            user_context = ""

    # quotes = await quote_service.get_random_by_source_type(
    #     db, source_type=source_type, limit=limit
    # )

    # if quotes:
    #     return quotes

    # Fallback to AI if no quotes found in DB
    if ai_service:
        # Get a larger pool from AI (cached)
        # We ignore the 'limit' param for the AI call to get the full pool
        ai_quotes_pool = await ai_service.get_recommendations(source_type, limit=15, user_context=user_context)
        
        if ai_quotes_pool:
            print(f"DEBUG RECOM: Pool size from AI: {len(ai_quotes_pool)}, Requested Limit: {limit}")
            # Randomly select 'limit' (3) items from the pool
            # This ensures variety on every refresh
            if len(ai_quotes_pool) > limit:
                ai_quotes = random.sample(ai_quotes_pool, limit)
            else:
                ai_quotes = ai_quotes_pool
            
            print(f"DEBUG RECOM: Selected {len(ai_quotes)} quotes")

            # Shuffle again just in case (random.sample already does it but good practice)
            random.shuffle(ai_quotes)

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
                
                # Construct dummy source - Expecting real data from AI now
                source_read = SourceRead(
                    id=0,
                    title=q.get("source_title", "Unknown"),
                    source_type=source_type,
                    creator=q.get("author", "Unknown"),
                    created_at=datetime.now()
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
            
@router.post("/related", response_model=List[QuoteRead])
async def get_related_recommendations(
    current_quote_content: str = Body(..., embed=True),
    limit: int = 3,
):
    """
    Get recommendations related to a specific quote content.
    Used for "Chain Recommendation" on Detail page.
    """
    if not ai_service:
        return []

    print(f"DEBUG RECOM: Generating Chain Recommendations for: {current_quote_content[:30]}...")
    
    # Call AI Service for related quotes
    # Context is just the current quote content
    related_quotes = await ai_service.get_related_quotes(current_quote_content, limit=limit)
    
    from app.schemas.source import SourceRead
    from app.schemas.tag import TagRead
    from datetime import datetime
    
    recommendations = []
    for i, q in enumerate(related_quotes):
        # Using negative ID to indicate it's not a real DB record
        fake_id = -1000 - i # Start from -1000 to differentiate? or just negative
        
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
        
        # Construct dummy source - Expecting real data from AI now
        source_read = SourceRead(
            id=0,
            title=q.get("source_title", "Unknown"),
            source_type=q.get("source_type", "book"),
            creator=q.get("author", "Unknown"),
            created_at=datetime.now()
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


from app.schemas.recommendation import BookRecommendation

# ...

@router.post("/ai", response_model=List[BookRecommendation])
async def get_ai_recommendations(
    refresh: bool = Query(False),
    db: AsyncSession = Depends(get_async_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Get AI-based book recommendations using Vertex AI (Gemini).
    It calls the AI service with the user's recent bookmarks and quotes as context.
    """
    if not ai_service:
        # Return empty list instead of string error to match model
        return []
    
    # ... (context gathering logic)

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
    recommendations = await ai_service.generate_book_recommendations(user_context, bypass_cache=refresh)
    
    return recommendations
