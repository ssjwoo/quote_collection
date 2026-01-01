import logging
import json
import aiohttp
from typing import Any, Optional

logger = logging.getLogger(__name__)

class AladinClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://www.aladin.co.kr/ttb/api/ItemSearch.aspx"

    async def fetch_book_info(self, title: str, author: str, session: Optional[aiohttp.ClientSession] = None) -> dict:
        """Fetch book cover and link from Aladin API."""
        if not self.api_key:
            return {"image": "", "link": ""}
        
        query = f"{title} {author}".strip()
        params = {
            "ttbkey": self.api_key,
            "Query": query,
            "QueryType": "Keyword",
            "MaxResults": "1",
            "start": "1",
            "SearchTarget": "Book",
            "output": "js",
            "Version": "20131101"
        }

        try:
            if session:
                return await self._do_fetch(session, params)
            else:
                async with aiohttp.ClientSession() as new_session:
                    return await self._do_fetch(new_session, params)
        except Exception as e:
            logger.warning(f"Aladin API error for {query}: {e}")
            return {"image": "", "link": ""}

    async def _do_fetch(self, session: aiohttp.ClientSession, params: dict) -> dict:
        async with session.get(self.base_url, params=params, timeout=5) as response:
            if response.status != 200:
                return {"image": "", "link": ""}
            
            data = await response.json()
            items = data.get("item", [])
            if not items:
                return {"image": "", "link": ""}
            
            item = items[0]
            image = item.get("cover", "")
            if image:
                image = image.replace("http://", "https://")
                # Scale up thumbnail to full cover if possible
                for thumb in ["sum.jpg", "ssum.jpg"]:
                    if thumb in image:
                        image = image.replace(thumb, "cover500.jpg")
            
            return {
                "image": image,
                "link": item.get("link", "")
            }
