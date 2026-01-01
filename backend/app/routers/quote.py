from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.schemas.pagination import PaginatedResponse
import math

from app.database import get_async_db
from app.schemas.quote import QuoteCreate, QuoteRead, QuoteUpdate, QuoteBase
from app.schemas.tag import TagCreate
from app.schemas.popular import PopularQuoteResponse
from app.services import quote_service, user_service, source_service, tag_service
from app.models import Quote
from app.models.quote_tag import quote_tags

router = APIRouter(prefix="/quote", tags=["Quote"])


import sys
import os
from app.core.config import settings
# Add project root to sys.path for llm import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../llm")))

try:
    from ai_service import AIService
except ImportError:
    AIService = None

# Initialize AIService
ai_service = AIService(
    project_id=settings.google_project_id, 
    location="us-central1",
    aladin_api_key=settings.aladin_api_key
) if AIService else None


@router.get("/popular/today/{source_type}", response_model=PopularQuoteResponse)
async def get_todays_popular_quote(
    source_type: str, db: AsyncSession = Depends(get_async_db)
):
    print(f"DEBUG: get_todays_popular_quote called for {source_type}")
    # Always use 'book' regardless of input
    popular_quote = await quote_service.get_todays_most_popular_by_source_type(
        db, source_type="book"
    )
    
    if popular_quote:
        print(f"DEBUG source={source_type}: Found DB quote: {popular_quote}")
        return popular_quote

    print(f"DEBUG source={source_type}: No DB quote found. Checking AI Service...")

    # Fallback to AI if no popular quote found
    if ai_service:
        print(f"DEBUG: AI Service IS available.")
        daily_quote_data = await ai_service.get_daily_quote(source_type)
        print(f"DEBUG: AI Service returned: {daily_quote_data}")
        if daily_quote_data:
            tags_data = daily_quote_data.get("tags", [])
            tag_list = []
            if isinstance(tags_data, list):
                 from app.schemas.tag import TagRead
                 # TagRead requires id, name, created_at. We can use a simplified dict or obj.
                 # Actually PopularQuoteResponse defines tags as list | None. 
                 # Let's verify what the frontend expects. 
                 # The frontend BookDetail expects quote.tags to be a list of objects with 'name' property.
                 # So we can just pass a list of dicts or TagRead objects.
                 # Let's pass list of dicts for simplicity if pydantic allows, or TagRead.
                 # But TagRead structure is safer.
                 from datetime import datetime
                 for i, t in enumerate(tags_data):
                     tag_list.append({
                         "id": -1 * (i + 1),
                         "name": str(t),
                         "created_at": datetime.now()
                     })

            return PopularQuoteResponse(
                id=0, # Placeholder ID
                title=daily_quote_data.get("source_title", "Unknown Source"),
                content=daily_quote_data.get("content", ""),
                creator=daily_quote_data.get("author", "Unknown Author"),
                tags=tag_list
            )

    print(f"DEBUG: AI Service not available or returned None. Import Error: {AI_IMPORT_ERROR}")
    print(f"DEBUG: Current sys.path: {sys.path}")
    raise HTTPException(status_code=404, detail=f"No popular quote found. AI Error: {AI_IMPORT_ERROR}")


@router.get("/latest", response_model=list[QuoteRead])
async def get_latest_quotes(
    source_type: str = "book", db: AsyncSession = Depends(get_async_db)
):
    return await quote_service.get_latest_by_source_type(db, source_type=source_type)


@router.post("/", response_model=QuoteRead)
async def create_quote(quote_in: QuoteCreate, db: AsyncSession = Depends(get_async_db)):
    user = await user_service.repository.get(db, id=quote_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    source = await source_service.repository.get(db, id=quote_in.source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    tag_names = quote_in.tags

    class QuoteCreateInternal(QuoteBase):
        pass

    quote_data = quote_in.model_dump()
    if 'tags' in quote_data:
        del quote_data['tags']

    quote_to_create = QuoteCreateInternal(**quote_data)

    try:
        # This creates, commits, and refreshes the quote. The returned object is expired.
        created_quote = await quote_service.repository.create(
            db, obj_in=quote_to_create
        )
        quote_id = created_quote.id

        if tag_names:
            tag_ids_to_associate = []
            for name in tag_names:
                tag = await tag_service.repository.get_by_name(db, name=name)
                if not tag:
                    # This also creates, commits, and refreshes.
                    tag = await tag_service.repository.create(
                        db, obj_in=TagCreate(name=name)
                    )
                tag_ids_to_associate.append(tag.id)

            if tag_ids_to_associate:
                associations = [
                    {"quote_id": quote_id, "tag_id": tag_id}
                    for tag_id in tag_ids_to_associate
                ]
                await db.execute(quote_tags.insert().values(associations))
                await db.commit()

        # Re-fetch the quote with the tags preloaded to return the correct data.
        result = await db.execute(
            select(Quote)
            .where(Quote.id == quote_id)
            .options(selectinload(Quote.tags), selectinload(Quote.source))
        )
        final_quote = result.scalar_one()
        return final_quote

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Database integrity issue: {e}"
        )


@router.get("/", response_model=list[QuoteRead])
async def list_quotes(db: AsyncSession = Depends(get_async_db)):
    return await quote_service.repository.get_all(db)


@router.get("/{quote_id}", response_model=QuoteRead)
async def get_quote(quote_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(
        select(Quote)
        .options(selectinload(Quote.source), selectinload(Quote.tags))
        .filter(Quote.id == quote_id)
    )
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.get("/user/{user_id}", response_model=PaginatedResponse[QuoteRead])
async def get_quotes_by_user(
    user_id: int, 
    page: int = 1, 
    size: int = 10, 
    db: AsyncSession = Depends(get_async_db)
):
    items, total = await quote_service.get_by_user_id_paginated(db, user_id=user_id, page=page, size=size)
    total_pages = math.ceil(total / size) if total > 0 else 0
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        total_pages=total_pages
    )


@router.put("/{quote_id}", response_model=QuoteRead)
async def update_quote(
    quote_id: int, quote_in: QuoteUpdate, db: AsyncSession = Depends(get_async_db)
):
    quote = await quote_service.repository.get(db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # Extract tags from the input, if present
    tag_names = quote_in.tags
    quote_data = quote_in.model_dump(exclude_unset=True)
    if 'tags' in quote_data:
        del quote_data['tags']

    # Update quote's basic fields
    updated_quote = await quote_service.repository.update(db, db_obj=quote, obj_in=quote_data)

    # Handle tags update
    if tag_names is not None: # Check if tags were explicitly provided in the update
        # Delete existing associations
        await db.execute(quote_tags.delete().where(quote_tags.c.quote_id == quote_id))

        if tag_names: # If new tags are provided, create new associations
            tag_ids_to_associate = []
            for name in tag_names:
                tag = await tag_service.repository.get_by_name(db, name=name)
                if not tag:
                    tag = await tag_service.repository.create(db, obj_in=TagCreate(name=name))
                tag_ids_to_associate.append(tag.id)

            if tag_ids_to_associate:
                associations = [
                    {"quote_id": quote_id, "tag_id": tag_id}
                    for tag_id in tag_ids_to_associate
                ]
                await db.execute(quote_tags.insert().values(associations))
        await db.commit() # Commit after tag operations

    # Re-fetch the quote with the updated tags preloaded to return the correct data.
    result = await db.execute(
        select(Quote)
        .where(Quote.id == quote_id)
        .options(selectinload(Quote.tags), selectinload(Quote.source))
    )
    final_quote = result.scalar_one()
    return final_quote


@router.delete("/{quote_id}")
async def delete_quote(quote_id: int, db: AsyncSession = Depends(get_async_db)):
    quote = await quote_service.repository.get(db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=400, detail="문장을 찾을 수 없습니다.")
    await quote_service.repository.remove(db, id=quote_id)
    return {"message": "문장 삭제 됨"}
