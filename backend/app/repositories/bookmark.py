from app.models import Bookmark
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
        return result.scalar_one_or_none()

    async def remove(self, db: AsyncSession, *, id: Any) -> Bookmark | None:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def get_by_user_id(self, db: AsyncSession, *, user_id: int) -> list[Bookmark]:
        statement = (
            select(self.model)
            .options(selectinload(self.model.quote))
            .filter(self.model.user_id == user_id)
        )
        result = await db.execute(statement)
        return result.scalars().all()


bookmark_repository = BookmarkRepository(Bookmark)
