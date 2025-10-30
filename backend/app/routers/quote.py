from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database import get_async_db
from app.schemas import QuoteCreate, QuoteRead, QuoteUpdate
from app.schemas.popular import PopularQuoteResponse
from app.services import quote_service, user_service, source_service

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
async def create_quote(quote: QuoteCreate, db: AsyncSession = Depends(get_async_db)):
    user = await user_service.repository.get(db, id=quote.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    source = await source_service.repository.get(db, id=quote.source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    try:
        return await quote_service.repository.create(db, obj_in=quote)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Database integrity issue: {e}")

@router.get("/", response_model=list[QuoteRead])
async def list_quotes(db: AsyncSession = Depends(get_async_db)):
    return await quote_service.repository.get_all(db)

@router.get("/{quote_id}", response_model=QuoteRead)
async def get_quote(quote_id: int, db: AsyncSession = Depends(get_async_db)):
    quote = await quote_service.get_by_id_with_source_type(db, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    # SQLAlchemy -> dict 변환
    quote_dict = {
        "id": quote.id,
        "content": quote.content,
        "page": quote.page,
        "source_id": quote.source_id,
        "user_id": quote.user_id,
        "created_at": quote.created_at,
        "source_type": getattr(quote, "source_type", None),
    }

    return quote_dict

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

@router.get("/user/{user_id}", response_model=List[QuoteRead])
async def get_quotes_by_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    return await quote_service.get_by_user_id(db, user_id=user_id)
