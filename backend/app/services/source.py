from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.repositories import source_repository, book_repository, movie_repo, drama_repo
from app.schemas import SourceRead, BookRead, MovieRead, DramaRead

class SourceService(BaseService):
    async def get_with_details(self, db: AsyncSession, source_id: int) -> SourceRead | None:
        source = await self.repository.get(db, id=source_id)
        if not source:
            return None
        await db.refresh(source) # Ensure all attributes are loaded

        details = None
        if source.source_type == 'book' and source.details_id:
            book_obj = await book_repository.get(db, id=source.details_id)
            if book_obj: details = BookRead.model_validate(book_obj)
        elif source.source_type == 'movie' and source.details_id:
            movie_obj = await movie_repo.get(db, id=source.details_id)
            if movie_obj: details = MovieRead.model_validate(movie_obj)
        elif source.source_type == 'tv' and source.details_id:
            drama_obj = await drama_repo.get(db, id=source.details_id)
            if drama_obj: details = DramaRead.model_validate(drama_obj)
        
        source_read = SourceRead.model_validate(source)
        source_read.details = details
        return source_read

    async def get_all_with_details(self, db: AsyncSession) -> list[SourceRead]:
        sources = await self.repository.get_all(db)
        sources_with_details = []
        for source in sources:
            source_with_details = await self.get_with_details(db, source.id)
            if source_with_details:
                sources_with_details.append(source_with_details)
        return sources_with_details

    async def update(self, db: AsyncSession, *, db_obj, obj_in) -> SourceRead:
        updated_obj = await self.repository.update(db, db_obj=db_obj, obj_in=obj_in)
        return await self.get_with_details(db, source_id=updated_obj.id)

source_service = SourceService(source_repository)
