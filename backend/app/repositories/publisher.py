from app.models import Publisher
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class PublisherRepository(BaseRepository[Publisher]):
    async def get_by_name(self, db: AsyncSession, name: str) -> Publisher | None:
        statement = select(self.model).filter(self.model.name == name)
        result = await db.execute(statement)
        return result.scalar_one_or_none()


publisher_repository = PublisherRepository(Publisher)
