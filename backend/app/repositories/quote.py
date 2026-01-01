from sqlalchemy import func, desc, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, time, timedelta
from sqlalchemy.orm import selectinload

from app.models import Quote, Bookmark, Source, Tag
from app.repositories.base import BaseRepository


class QuoteRepository(BaseRepository[Quote]):
    async def get_most_bookmarked(self, db: AsyncSession, limit: int = 10) -> list[Quote]:
        statement = (
            select(self.model)
            .join(Bookmark, self.model.id == Bookmark.quote_id)
            .options(selectinload(self.model.source), selectinload(self.model.tags))
            .group_by(self.model.id)
            .order_by(func.count(Bookmark.quote_id).desc())
            .limit(limit)
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def search(self, db: AsyncSession, query: str, source_type: str | None = None, limit: int = 10) -> list[Quote]:
        statement = (
            select(self.model)
            .outerjoin(self.model.tags)
            .filter(
                or_(
                    self.model.content.ilike(f"%{query}%"),
                    Tag.name.ilike(f"%{query}%")
                )
            )
        )
        if source_type:
            statement = statement.join(Source).filter(Source.source_type == source_type)

        statement = statement.options(selectinload(self.model.source), selectinload(self.model.tags)).distinct().limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_by_user_id(self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 10) -> list[Quote]:
        statement = (
            select(self.model)
            .options(selectinload(self.model.source), selectinload(self.model.tags))
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc()) # 최신순
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def count_by_user_id(self, db: AsyncSession, *, user_id: int) -> int:
        statement = select(func.count()).select_from(self.model).filter(self.model.user_id == user_id)
        result = await db.execute(statement)
        return result.scalar() or 0

    async def get_by_source_id(self, db: AsyncSession, *, source_id: int) -> list[Quote]:
        statement = (
            select(self.model)
            .options(selectinload(self.model.source), selectinload(self.model.tags))
            .filter(self.model.source_id == source_id)
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_latest_by_source_type(
        self, db: AsyncSession, *, source_type: str, limit: int = 10
    ) -> list[Quote]:
        statement = (
            select(self.model)
            .join(Source)
            .filter(Source.source_type == source_type)
            .options(selectinload(self.model.source), selectinload(self.model.tags))
            .order_by(desc(self.model.created_at))
            .limit(limit)
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_random_by_source_type(
        self, db: AsyncSession, *, source_type: str, limit: int = 3
    ) -> list[Quote]:
        statement = (
            select(self.model)
            .join(Source)
            .filter(Source.source_type == source_type)
            .options(selectinload(self.model.source), selectinload(self.model.tags))
            .order_by(func.random())
            .limit(limit)
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_todays_most_popular_by_source_type(
        self, db: AsyncSession, *, source_type: str
    ) -> tuple[Quote, Source] | None:
        today = datetime.utcnow().date()

        for i in range(365):  # check for the last year
            target_date = today - timedelta(days=i)
            start_of_day = datetime.combine(target_date, time.min)
            end_of_day = datetime.combine(target_date, time.max)

            statement = (
                select(self.model, Source)
                .join(Bookmark, self.model.id == Bookmark.quote_id)
                .join(Source, self.model.source_id == Source.id)
                .filter(Source.source_type == source_type)
                .filter(Bookmark.created_at >= start_of_day)
                .filter(Bookmark.created_at <= end_of_day)
                .group_by(self.model.id, Source.id)
                .order_by(func.count(Bookmark.quote_id).desc())
                .limit(1)
            )
            result = await db.execute(statement)
            popular_quote = result.first()
            if popular_quote:
                return popular_quote

        return None


quote_repository = QuoteRepository(Quote)
