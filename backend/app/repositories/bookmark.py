from app.models import Bookmark, Quote
from app.repositories.base import BaseRepository
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Any

class BookmarkRepository(BaseRepository[Bookmark]):
    async def get(self, db: AsyncSession, id: Any) -> Bookmark | None:
        user_id, quote_id = id
        statement = select(self.model).filter_by(user_id=user_id, quote_id=quote_id)
        result = await db.execute(statement)
        return result.scalars().first()

    async def remove(self, db: AsyncSession, *, id: Any) -> Bookmark | None:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def get_by_user_id(self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 10) -> list[Bookmark]:
        statement = (
            select(self.model)
            .options(
                selectinload(self.model.quote).selectinload(Quote.source),
                selectinload(self.model.quote).selectinload(Quote.tags)
            )
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc()) # 최신순 기본 정합성
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def count_by_user_id(self, db: AsyncSession, *, user_id: int) -> int:
        from sqlalchemy import func
        statement = select(func.count()).select_from(self.model).filter(self.model.user_id == user_id)
        result = await db.execute(statement)
        return result.scalar() or 0


bookmark_repository = BookmarkRepository(Bookmark)
