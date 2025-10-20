from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import quote_repository, source_repository, tag_repository
from app.schemas import SearchResult
from app.services.source import source_service # Import source_service

class SearchService:
    async def search(self, db: AsyncSession, query: str) -> SearchResult:
        quotes = await quote_repository.search(db, query=query)
        raw_sources = await source_repository.search(db, query=query)
        sources_with_details = []
        for source in raw_sources:
            source_with_details = await source_service.get_with_details(db, source_id=source.id)
            if source_with_details:
                sources_with_details.append(source_with_details)
        tags = await tag_repository.search(db, query=query)
        return SearchResult(quotes=quotes, sources=sources_with_details, tags=tags)

search_service = SearchService()
