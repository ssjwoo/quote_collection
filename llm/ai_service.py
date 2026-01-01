import logging
import json
import asyncio
import hashlib
import random
import urllib.parse
from datetime import datetime
from typing import Any, Optional, List, Dict

from vertex_client import VertexAIClient, _ensure_vertex_libs
from aladin_client import AladinClient
from prompts import (
    BOOK_RECOMMENDATION_PROMPT,
    DAILY_QUOTE_PROMPT,
    GENERIC_RECOMMENDATION_PROMPT,
    RELATED_QUOTE_PROMPT
)

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, project_id: str, location: str = "us-central1", aladin_api_key: str = ""):
        # Force us-central1 for Gemini 2.0 stability as per user's previous stable state
        self.vertex = VertexAIClient(project_id, "us-central1")
        self.aladin = AladinClient(aladin_api_key)
        self._cache = {}
        logger.info("AIService Initialized (Refactored).")

    def _get_cache_key(self, prefix: str, *args) -> tuple:
        return (prefix, *args)

    async def _generate_json(self, prompt: str, model_name: str = "gemini-2.0-flash") -> Any:
        """Helper to generate and parse JSON safely."""
        logger.info(f"Generating JSON with model {model_name}. Prompt length: {len(prompt)}")
        try:
            raw_text = await self.vertex.generate_content(
                prompt, 
                model_name=model_name,
                generation_config={"response_mime_type": "application/json"}
            )
            if not raw_text:
                logger.warning(f"AI returned empty response for model {model_name}")
                return None
            
            logger.debug(f"Raw AI response: {raw_text[:200]}...")
            
            # Basic cleanup if AI ignores mime_type or wraps in markdown
            text = raw_text.strip()
            if text.startswith("```json"): text = text[7:]
            if text.endswith("```"): text = text[:-3]
            
            # Find JSON boundaries
            start = text.find('[') if '[' in text else text.find('{')
            end = text.rfind(']') if ']' in text else text.rfind('}')
            if start != -1 and end != -1:
                text = text[start : end + 1]
            
            parsed = json.loads(text)
            logger.info(f"Successfully parsed AI response. Type: {type(parsed)}")
            return parsed
        except Exception as e:
            logger.error(f"JSON Generation/Parsing error (Model: {model_name}): {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None

    async def generate_book_recommendations(self, user_context: str, bypass_cache: bool = False) -> List[Dict]:
        time_window = datetime.now().strftime("%Y-%m-%d-%H")
        cache_key = self._get_cache_key("books", time_window, user_context[:100])
        
        if not bypass_cache and cache_key in self._cache:
            return self._cache[cache_key]

        prompt = BOOK_RECOMMENDATION_PROMPT.format(
            user_context=user_context or "신규 사용자입니다. 명작을 추천해주세요."
        )
        
        books = await self._generate_json(prompt, model_name="gemini-2.0-flash")
        if not books:
            return []

        if not isinstance(books, list):
            books = [books] if isinstance(books, dict) else []

        # Enrich with Aladin info in parallel
        import aiohttp
        async with aiohttp.ClientSession() as session:
            tasks = [self.aladin.fetch_book_info(b.get('title', ''), b.get('author', ''), session) for b in books]
            aladin_results = await asyncio.gather(*tasks)
            
            for book, info in zip(books, aladin_results):
                book['image'] = info.get('image', '')
                book['link'] = info.get('link') or f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord={urllib.parse.quote(book.get('title', ''))}"

        self._cache[cache_key] = books
        return books

    async def get_daily_quote(self, source_type: str) -> Dict:
        today = datetime.now().strftime("%Y-%m-%d")
        cache_key = self._get_cache_key("daily", source_type, today)
        
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = DAILY_QUOTE_PROMPT.format(source_type=source_type, today=today)
        quote = await self._generate_json(prompt)
        
        if not quote:
            # Absolute fallback
            return {
                "content": "가장 훌륭한 시는 아직 쓰여지지 않았다.",
                "source_title": "나짐 히크메트 시집",
                "author": "나짐 히크메트",
                "source_type": source_type,
                "tags": ["희망", "시"]
            }

        self._cache[cache_key] = quote
        return quote

    async def get_recommendations(self, source_type: str, limit: int = 3, user_context: str = "") -> List[Dict]:
        time_window = datetime.now().strftime("%Y-%m-%d-%H")
        context_hash = hashlib.md5(user_context.encode()).hexdigest() if user_context else "default"
        cache_key = self._get_cache_key("recom_pool", source_type, time_window, context_hash)

        if cache_key in self._cache:
            pool = self._cache[cache_key]
        else:
            prompt = GENERIC_RECOMMENDATION_PROMPT.format(
                pool_size=limit, # Match limit for precise mixture ratio
                user_context=user_context or "General audience", 
                source_type=source_type
            )
            pool = await self._generate_json(prompt)
            if not pool: return []
            self._cache[cache_key] = pool

        if not isinstance(pool, list): pool = [pool] if isinstance(pool, dict) else []
        
        # If pool size matches limit exactly, just return it (mixture handled by prompt)
        if len(pool) == limit:
            selected = pool
        else:
            selected = random.sample(pool, min(len(pool), limit))
        # Ensure links exist
        for item in selected:
            if not item.get('link'):
                q = f"{item.get('source_title', '')} {item.get('author', '')}".strip()
                item['link'] = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord={urllib.parse.quote(q)}"
            item['image'] = item.get('image', '')
            
        return selected

    async def get_related_quotes(self, current_quote_content: str, limit: int = 3) -> List[Dict]:
        prompt = RELATED_QUOTE_PROMPT.format(
            current_quote_content=current_quote_content,
            limit=limit
        )
        related = await self._generate_json(prompt)
        if not related: return []
        if not isinstance(related, list): related = [related]
        
        # Add basic enrichment
        for item in related:
            q = f"{item.get('source_title', '')} {item.get('author', '')}".strip()
            item['link'] = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord={urllib.parse.quote(q)}"
            item['image'] = ""
            
        return related
