import logging
import random
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import QuoteRead, UserResponse
from app.schemas.source import SourceRead
from app.schemas.tag import TagRead
from app.schemas.recommendation import BookRecommendation
from app.services import bookmark_service, quote_service

logger = logging.getLogger(__name__)

class AIRecommendationService:
    def __init__(self, ai_service):
        self.ai_service = ai_service

    async def get_user_context(self, db: AsyncSession, user_id: int) -> str:
        """Gather recent bookmarks and quotes for user context."""
        try:
            bookmarks = await bookmark_service.get_by_user_id(db, user_id=user_id)
            user_quotes = await quote_service.get_by_user_id(db, user_id=user_id)
            
            context_parts = []
            if bookmarks:
                context_parts.append("--- User Bookmarks ---")
                for b in bookmarks[:10]:
                    q = b.quote
                    source_title = q.source.title if q.source and q.source.title else "Unknown"
                    context_parts.append(f"- Source: {source_title}, Content: {q.content[:50]}")
            
            if user_quotes:
                context_parts.append("--- User Created Quotes ---")
                for q in user_quotes[:10]:
                    source_title = q.source.title if q.source and q.source.title else "Unknown"
                    context_parts.append(f"- Source: {source_title}, Content: {q.content[:50]}")
            
            return "\n".join(context_parts)
        except Exception as e:
            logger.error(f"Failed to build user context: {e}")
            return ""

    async def get_quotes_recommendations(self, db: AsyncSession, source_type: str, limit: int, user_id: Optional[int] = None) -> List[QuoteRead]:
        """Fetch and transform AI quote recommendations."""
        if not self.ai_service:
            return []

        user_context = await self.get_user_context(db, user_id) if user_id else ""
        
        # Get pool from AI
        ai_quotes_pool = await self.ai_service.get_recommendations(source_type, limit=15, user_context=user_context)
        if not ai_quotes_pool:
            return []

        # Variety selection
        selected = random.sample(ai_quotes_pool, min(len(ai_quotes_pool), limit))
        
        recommendations = []
        for i, q in enumerate(selected):
            recommendations.append(self._to_quote_read(q, source_type, -1 * (i + 1)))
        
        return recommendations

    async def get_related_chain(self, current_content: str, limit: int) -> List[QuoteRead]:
        """Fetch chain recommendations."""
        if not self.ai_service:
            return []
        
        related_raw = await self.ai_service.get_related_quotes(current_content, limit=limit)
        
        recommendations = []
        for i, q in enumerate(related_raw):
            recommendations.append(self._to_quote_read(q, q.get("source_type", "book"), -1000 - i))
        
        return recommendations

    def _to_quote_read(self, ai_data: dict, source_type: str, fake_id: int) -> QuoteRead:
        """Convert raw AI dict to QuoteRead schema."""
        tags_list = []
        for t_idx, t_name in enumerate(ai_data.get("tags", [])):
            tags_list.append(TagRead(
                id=-1 * (t_idx + 1),
                name=str(t_name),
                created_at=datetime.now()
            ))
        
        source_read = SourceRead(
            id=0,
            title=ai_data.get("source_title", "Unknown"),
            source_type=source_type,
            creator=ai_data.get("author", "Unknown"),
            created_at=datetime.now()
        )
        
        return QuoteRead(
            id=fake_id,
            content=ai_data.get('content', ''),
            source_id=0,
            user_id=0,
            created_at=datetime.now(),
            tags=tags_list,
            source=source_read
        )
