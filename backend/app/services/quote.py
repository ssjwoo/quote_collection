from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import quote_repository
from app.services.base import BaseService
from app.repositories.quote import QuoteRepository
from app.schemas.popular import PopularQuoteResponse


class QuoteService(BaseService[QuoteRepository]):
    async def get_most_bookmarked(self, db: AsyncSession, limit: int = 10):
        return await self.repository.get_most_bookmarked(db, limit=limit)

    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        return await self.repository.get_by_user_id(db, user_id=user_id)

    async def get_latest_by_source_type(
        self, db: AsyncSession, source_type: str, limit: int = 10
    ):
        return await self.repository.get_latest_by_source_type(
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


quote_service = QuoteService(quote_repository)
