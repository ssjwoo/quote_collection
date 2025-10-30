from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Tag
from app.repositories.base import BaseRepository


class TagRepository(BaseRepository[Tag]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Tag | None:
        statement = select(self.model).filter(self.model.name == name)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def search(self, db: AsyncSession, query: str, limit: int = 10) -> list[Tag]:
        statement = (
            select(self.model)
            .filter(self.model.name.ilike(f"%{query}%"))
            .limit(limit)
        )
        result = await db.execute(statement)
        return result.scalars().all()


tag_repository = TagRepository(Tag)
