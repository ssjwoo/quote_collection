from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories import quote_repository
from app.services.base import BaseService
from app.repositories.quote import QuoteRepository
from app.schemas.popular import PopularQuoteResponse
from app.models.quote import Quote
from app.models.source import Source


class QuoteService(BaseService[QuoteRepository]):
    async def get_most_bookmarked(self, db: AsyncSession, limit: int = 10):
        return await self.repository.get_most_bookmarked(db, limit=limit)
    
    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(Quote).where(Quote.user_id == user_id))
        quotes = result.scalars().all()
        return quotes

    async def get_latest_by_source_type(
        self, db: AsyncSession, source_type: str, limit: int = 10
    ):
        return await self.repository.get_latest_by_source_type(
            db, source_type=source_type, limit=limit
        )

    async def get_random_by_source_type(
        self, db: AsyncSession, source_type: str, limit: int = 3
    ):
        return await self.repository.get_random_by_source_type(
            db, source_type=source_type, limit=limit
        )
    async def get_todays_most_popular_by_source_type(
        self, db: AsyncSession, source_type: str
    ) -> PopularQuoteResponse | None:
        result = await self.repository.get_todays_most_popular_by_source_type(
            db, source_type=source_type
        )
        if not result:
            return None

        quote, source = result
        return PopularQuoteResponse(
            id=quote.id,
            title=source.title,
            content=quote.content,
            creator=source.creator,
        )

    async def get_by_id_with_source_type(self, db: AsyncSession, quote_id: int):
        query = (
            select(Quote, Source.source_type)
            .join(Source, Quote.source_id == Source.id)
            .where(Quote.id == quote_id)
        )
        result = await db.execute(query)
        row = result.first()
        if not row:
            return None

        quote, source_type = row
        quote.source_type = source_type
        return quote

quote_service = QuoteService(quote_repository)
