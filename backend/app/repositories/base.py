from typing import Any, Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base
from sqlalchemy.future import select

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> ModelType | None:
        statement = select(self.model).filter(self.model.id == id)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> list[ModelType]:
        statement = select(self.model)
        result = await db.execute(statement)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in) -> ModelType:
        db_obj = self.model(**obj_in.model_dump(exclude_none=True))
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj, obj_in) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        print(f"Update data in BaseRepository.update: {update_data}") # Debug print
        if not update_data:
            return db_obj # No data to update

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj) # Explicitly add to session
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        obj = await self.get(db, id)
        await db.delete(obj)
        await db.commit()
        return obj