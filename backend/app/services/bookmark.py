from app.repositories import bookmark_repository
from app.services.base import BaseService
from app.repositories.bookmark import BookmarkRepository
from sqlalchemy.ext.asyncio import AsyncSession


class BookmarkService(BaseService[BookmarkRepository]):
    async def get_by_user_id_paginated(self, db: AsyncSession, user_id: int, page: int = 1, size: int = 10):
        skip = (page - 1) * size
        items = await self.repository.get_by_user_id(db, user_id=user_id, skip=skip, limit=size)
        total = await self.repository.count_by_user_id(db, user_id=user_id)
        return items, total


bookmark_service = BookmarkService(bookmark_repository)
