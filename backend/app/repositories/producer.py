from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Producer
from app.repositories.base import BaseRepository


class ProducerRepository(BaseRepository[Producer]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Producer | None:
        statement = select(self.model).filter(self.model.name == name)
        result = await db.execute(statement)
        return result.scalar_one_or_none()


producer_repository = ProducerRepository(Producer)
