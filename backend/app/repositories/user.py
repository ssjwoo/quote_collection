from app.models import User
from app.repositories.base import BaseRepository
from app.schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import hash_password
from sqlalchemy.future import select


class UserRepository(BaseRepository[User]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        statement = select(User).filter(User.email == email)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=hash_password(obj_in.password),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


user_repository = UserRepository(User)
