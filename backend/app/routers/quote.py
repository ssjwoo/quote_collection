from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_async_db
from app.schemas.quote import QuoteCreate, QuoteRead, QuoteUpdate, QuoteBase
from app.schemas.tag import TagCreate
from app.schemas.popular import PopularQuoteResponse
from app.services import quote_service, user_service, source_service, tag_service
from app.models import Quote
from app.models.quote_tag import quote_tags

router = APIRouter(prefix="/quote", tags=["Quote"])


@router.get("/popular/today/{source_type}", response_model=PopularQuoteResponse)
async def get_todays_popular_quote(
    source_type: str, db: AsyncSession = Depends(get_async_db)
):
    popular_quote = await quote_service.get_todays_most_popular_by_source_type(
        db, source_type=source_type
    )
    if not popular_quote:
        raise HTTPException(status_code=404, detail="No popular quote found")
    return popular_quote


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
            select(Quote).where(Quote.id == quote_id).options(selectinload(Quote.tags))
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
    quote = await quote_service.repository.get(db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.put("/{quote_id}", response_model=QuoteRead)
async def update_quote(
    quote_id: int, quote_in: QuoteUpdate, db: AsyncSession = Depends(get_async_db)
):
    quote = await quote_service.repository.get(db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    quote = await quote_service.repository.update(db, db_obj=quote, obj_in=quote_in)
    return quote


@router.delete("/{quote_id}")
async def delete_quote(quote_id: int, db: AsyncSession = Depends(get_async_db)):
    quote = await quote_service.repository.get(db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=400, detail="문장을 찾을 수 없습니다.")
    await quote_service.repository.remove(db, id=quote_id)
    return {"message": "문장 삭제 됨"}
