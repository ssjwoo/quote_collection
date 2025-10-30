from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import quote_repository, source_repository, tag_repository
from app.schemas import SearchResult
from app.schemas.quote import QuoteRead as QuoteSchema
from app.schemas.source import SourceRead as SourceWithDetails
from app.services.source import source_service # Import source_service

class SearchService:
    async def search(self, db: AsyncSession, query: str, source_type: str | None = None) -> SearchResult:
        quotes = await quote_repository.search(db, query=query, source_type=source_type)
        raw_sources = await source_repository.search(db, query=query, source_type=source_type)
        tags = await tag_repository.search(db, query=query)

        all_source_ids = set()
        for source in raw_sources:
            all_source_ids.add(source.id)
        for quote in quotes:
            if quote.source_id:
                all_source_ids.add(quote.source_id)

        unique_sources_read = []
        processed_source_ids = set()
        for source_id in all_source_ids:
            if source_id not in processed_source_ids:
                source_with_details = await source_service.get_with_details(db, source_id=source_id)
                if source_with_details:
                    unique_sources_read.append(source_with_details)
                    processed_source_ids.add(source_id)
        
        quotes_read = []
        for quote in quotes:
            quotes_read.append(QuoteSchema.from_orm(quote))

        return SearchResult(quotes=quotes_read, sources=unique_sources_read, tags=tags)

search_service = SearchService()
