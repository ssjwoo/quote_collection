from app.repositories import bookmark_repository
from app.services.base import BaseService
from app.repositories.bookmark import BookmarkRepository
from sqlalchemy.ext.asyncio import AsyncSession


class BookmarkService(BaseService[BookmarkRepository]):
    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        return await self.repository.get_by_user_id(db, user_id=user_id)


bookmark_service = BookmarkService(bookmark_repository)
