from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Book, Drama, Movie, Producer, Source
from app.repositories.base import BaseRepository


class SourceRepository(BaseRepository[Source]):
    async def get_by_title_and_creator(self, db: AsyncSession, *, title: str, creator: str) -> Source | None:
        statement = select(Source).filter(Source.title == title, Source.creator == creator)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def search(self, db: AsyncSession, query: str, source_type: str | None = None, limit: int = 10) -> list[Source]:
        book_alias = aliased(Book)
        movie_alias = aliased(Movie)
        drama_alias = aliased(Drama)
        producer_alias = aliased(Producer)

        statement = (
            select(self.model)
            .outerjoin(book_alias, (self.model.source_type == "book") & (self.model.details_id == book_alias.id))
            .outerjoin(movie_alias, (self.model.source_type == "movie") & (self.model.details_id == movie_alias.id))
            .outerjoin(drama_alias, (self.model.source_type == "drama") & (self.model.details_id == drama_alias.id))
            .outerjoin(producer_alias, drama_alias.producer_id == producer_alias.id)
            .filter(
                or_(
                    self.model.title.ilike(f"%{query}%"),
                    self.model.creator.ilike(f"%{query}%"),
                    book_alias.author.ilike(f"%{query}%"),
                    movie_alias.director.ilike(f"%{query}%"),
                    producer_alias.name.ilike(f"%{query}%"),
                )
            )
        )

        if source_type:
            statement = statement.filter(self.model.source_type == source_type)

        statement = statement.limit(limit)
        result = await db.execute(statement)
        return result.scalars().unique().all()


source_repository = SourceRepository(Source)