import logging
import os
import sys

logger = logging.getLogger(__name__)

# Track if libraries are functional
_VERTEX_LIBS_READY = None 

def _ensure_vertex_libs():
    """Import Vertex AI libs safely"""
    global _VERTEX_LIBS_READY
    if _VERTEX_LIBS_READY is not None:
        return _VERTEX_LIBS_READY
    
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel, Tool
        try:
            from vertexai.generative_models import GoogleSearchRetrieval
            grounding = GoogleSearchRetrieval
        except ImportError:
            grounding = None
        
        _VERTEX_LIBS_READY = (vertexai, GenerativeModel, Tool, grounding)
        return _VERTEX_LIBS_READY
    except Exception as e:
        logger.error(f"Failed to load Vertex AI libraries: {e}")
        _VERTEX_LIBS_READY = False
        return False

class AIService:
    def __init__(self, project_id: str, location: str = "us-central1", aladin_api_key: str = ""):
        self.project_id = project_id
        self.location = "us-central1" # Force us-central1 for Gemini 2.0 stability
        self.aladin_api_key = aladin_api_key or os.getenv("ALADIN_API_KEY", "")
        self._model = None
        self._cache = {}
        logger.info(f"AIService Initialized. Cache ready: {hasattr(self, '_cache')}")
        print(f"DEBUG: AIService Initialized. Cache ready: {hasattr(self, '_cache')}")
        
    @property
    def model(self):
        if self._model:
            return self._model
        
        print(f"DEBUG AI: Attempting model access (Project={self.project_id}, Region={self.location})")
        libs = _ensure_vertex_libs()
        if not libs:
            print("DEBUG AI: Framework libraries failed to load.")
            return None
        
        vertexai, GenerativeModel, _, _ = libs
        
        # Priority 1: Gemini 2.0 Flash
        try:
            print(f"DEBUG AI: Initializing Gemini 2.0 Flash...")
            vertexai.init(project=self.project_id, location=self.location)
            self._model = GenerativeModel("gemini-2.0-flash")
            print("DEBUG AI: Gemini 2.0 Flash Initialized.")
            return self._model
        except Exception as e20:
            print(f"DEBUG AI: Gemini 2.0 Flash failed: {e20}. Trying Gemini 1.5 Flash...")
            
        # Priority 2: Gemini 1.5 Flash (More stable across regions)
        try:
            self._model = GenerativeModel("gemini-1.5-flash")
            print("DEBUG AI: Gemini 1.5 Flash Initialized as Fallback.")
            return self._model
        except Exception as e15:
            print(f"DEBUG AI: Gemini 1.5 Flash also failed: {e15}")
            logger.error(f"Vertex AI initialization failed for all models: {e15}")
            return None
    
    async def _fetch_aladin_book_info(self, title: str, author: str) -> dict:
        """Fetch book info from Aladin API"""
        print(f"DEBUG Aladin: Fetching book info for '{title}' by '{author}'")
        print(f"DEBUG Aladin: API Key exists: {bool(self.aladin_api_key)}")
        
        if not self.aladin_api_key:
            print("DEBUG Aladin: No API key, returning empty")
            return {"image": "", "link": ""}
        
        try:
            import aiohttp
            from urllib.parse import quote as url_quote
            
            query = f"{title} {author}".strip()
            url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
            params = {
                "ttbkey": self.aladin_api_key,
                "Query": query,
                "QueryType": "Keyword",
                "MaxResults": "1",
                "start": "1",
                "SearchTarget": "Book",
                "output": "js",
                "Version": "20131101"
            }
            
            print(f"DEBUG Aladin: Calling API with query: {query}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=5) as response:
                    print(f"DEBUG Aladin: Response status: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        print(f"DEBUG Aladin: Response data keys: {data.keys() if data else 'None'}")
                        if data.get("item") and len(data["item"]) > 0:
                            item = data["item"][0]
                            result = {
                                "image": item.get("cover", ""),
                                "link": item.get("link", "")
                            }
                            if result["image"]:
                                result["image"] = result["image"].replace("http://", "https://")
                                if "sum.jpg" in result["image"]:
                                    result["image"] = result["image"].replace("sum.jpg", "cover500.jpg")
                                elif "ssum.jpg" in result["image"]:
                                    result["image"] = result["image"].replace("ssum.jpg", "cover500.jpg")
                            
                            print(f"DEBUG Aladin: Found book - image: {result['image'][:50] if result['image'] else 'None'}, link: {result['link'][:50] if result['link'] else 'None'}")
                            return result
                        else:
                            print(f"DEBUG Aladin: No items in response")
            return {"image": "", "link": ""}
        except Exception as e:
            print(f"DEBUG Aladin: Exception occurred: {e}")
            logger.warning(f"Failed to fetch Aladin book info: {e}")
            return {"image": "", "link": ""}

    async def generate_book_recommendations(self, user_context: str, bypass_cache: bool = False) -> list[dict]:
        # Cache check
        if not hasattr(self, '_cache'):
            self._cache = {}
        
        from datetime import datetime
        # Use an hourly/daily window for cache to balance performance and variety
        time_window = datetime.now().strftime("%Y-%m-%d-%H")
        cache_key = ("book_recommendations", time_window, user_context[:200])
        
        if not bypass_cache and cache_key in self._cache:
            logger.info("Returning cached book recommendations")
            return self._cache[cache_key]

        libs = _ensure_vertex_libs()
        # Fallback if libraries missing or model init failed
        if not libs or not self.model:
             logger.warning("AI service not initialized or model failed. Returning empty list as requested.")
             return []
        
        _, GenerativeModel, Tool, grounding = libs

        try:
            if grounding:
                tool = Tool.from_google_search_retrieval(grounding())
            else:
                tool = None
        except Exception as e:
            logger.warning(f"GoogleSearchRetrieval not available: {e}. Proceeding without grounding.")
            tool = None

        prompt = f"""
        You are a smart AI book curator. Recommend 5 books based on the user's interests and current weather in Seoul, Korea.
        IMPORTANT: Provide UNIQUE, FRESH, and VARIED recommendations. Avoid repeating the same bestsellers.
        
        Step 1: Check current weather in Seoul, Korea.
        Step 2: Select 5 books that match the weather mood and user's interests.
        
        For each book, provide:
        - "title": Exact Korean book title (한글 제목)
        - "author": Author name (저자명)
        - "reason": Short explanation why this book is interesting/recommended. 
          IMPORTANT: DO NOT MENTION THE WEATHER OR MOOD EXPLICITLY IN THE REASON. 
          The reason should be about the book's content or vibe only.
        
        User's Interest Context:
        {user_context or "신규 사용자입니다. 일반적으로 인기있는 한국 문학 작품들을 추천해주세요."}
        
        Output ONLY raw JSON (no markdown, no explanation):
        [
            {{
                "title": "책 제목",
                "author": "저자명",
                "reason": "추천 이유"
            }},
            ...
        ]
        """

        try:
            # Use the tool for grounding with enforced JSON
            generate_kwargs = {
                "generation_config": {
                    "response_mime_type": "application/json",
                    "temperature": 1.2,
                    "top_p": 0.95,
                    "top_k": 40
                }
            }
            if tool:
                generate_kwargs["tools"] = [tool]
                
            response = await self.model.generate_content_async(
                prompt,
                **generate_kwargs
            )
            
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            start_index = text.find('[')
            end_index = text.rfind(']')
            
            if start_index != -1 and end_index != -1 and end_index > start_index:
                text = text[start_index : end_index + 1]
            else:
                logger.warning(f"Could not find JSON list in response: {text[:100]}...")
            
            import json
            from urllib.parse import quote as url_quote
            try:
                books = json.loads(text)
                if not isinstance(books, list):
                    if isinstance(books, dict):
                        books = [books]
                    else:
                        books = []
                
                for book in books:
                    title = book.get('title', '')
                    author = book.get('author', '')
                    
                    aladin_info = await self._fetch_aladin_book_info(title, author)
                    if aladin_info["link"]:
                        book['link'] = aladin_info["link"]
                    else:
                        search_query = f"{title} {author}".strip()
                        book['link'] = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={url_quote(search_query)}"
                    book['image'] = aladin_info["image"]
                    
                    book['image'] = aladin_info["image"]
                    
                self._cache[cache_key] = books
                return books
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON")
                return []
            
        except Exception as e:
            logger.error(f"Error generating content from Vertex AI: {e}")
            return []

    async def get_daily_quote(self, source_type: str) -> dict:
        if not self.model:
            logger.warning(f"AI Service not available. Returning mock quote for {source_type}")
            return {
                "content": "가장 훌륭한 시는 아직 쓰여지지 않았다. 가장 아름다운 노래는 아직 불려지지 않았다.",
                "source_title": "나짐 히크메트 시집",
                "author": "나짐 히크메트",
                "source_type": source_type,
                "tags": ["희망", "시", "미래"]
            }

        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        cache_key = ("daily_quote", source_type, today)

        if not hasattr(self, '_cache'):
            self._cache = {}

        if cache_key in self._cache:
            print(f"DEBUG AI: Returning cached daily quote for {source_type}")
            return self._cache[cache_key]

        print(f"DEBUG AI: Generating daily quote for {source_type}...")

        prompt = f"""
        Recommend a famous and inspiring quote from a {source_type} for today ({today}).
        
        The quote must be suitable for a general audience and widely recognized.
        
        Please provide the response in valid JSON format with the following keys:
        - content: The quote text (in Korean).
        - source_title: The title of the {source_type} (in Korean).
        - author: The author or character who said it (in Korean).
        - source_type: "{source_type}"
        - tags: A list of 1-3 keywords relevant to the quote (in Korean).

        Do not include markdown formatting (```json ... ```). Just the raw JSON string.
        """

        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            import json
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            start_index = text.find('{')
            end_index = text.rfind('}')
            if start_index != -1 and end_index != -1:
                text = text[start_index : end_index + 1]
                
            result = json.loads(text)
            self._cache[cache_key] = result
            return result
        except Exception as e:
            logger.error(f"Error generating daily quote: {e}")
            # Mock fallback on error too
            return {
                "content": "가장 훌륭한 시는 아직 쓰여지지 않았다.",
                "source_title": "나짐 히크메트 시집",
                "author": "나짐 히크메트",
                "source_type": source_type,
                "tags": ["희망", "시", "미래"]
            }

    async def get_recommendations(self, source_type: str, limit: int = 3, user_context: str = "") -> list[dict]:
        pool_size = 15  # Request a larger pool for diversity
        
        if not self.model:
             logger.warning(f"AI service not initialized. Returning empty list for {source_type}")
             return []

        from datetime import datetime
        # Include hour in cache key for hourly variety
        time_window = datetime.now().strftime("%Y-%m-%d-%H")
        cache_key = ("recommendations_pool", source_type, time_window, context_hash)

        # Initialize cache if missing (safety check)
        if not hasattr(self, '_cache'):
            self._cache = {}

        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = f"""
        Recommend {pool_size} famous and inspiring quotes from different {source_type}s.
        
        User's Interest/Context:
        {user_context or "General audience, popular and classic quotes."}

        The quotes must be suitable for the user's interest if provided, otherwise general audience.
        Only Korean.
        
        Please provide the response in valid JSON format as a LIST of objects with the following keys:
        - content: The quote text (in Korean).
        - source_title: The title of the {source_type} (in Korean).
        - author: The author or character who said it (in Korean).
        - source_type: "{source_type}"
        - tags: A list of 1-3 keywords relevant to the quote (in Korean), reflecting the user's interest if applicable.

        Do not include markdown formatting. Just the raw JSON list.
        """

        try:
            response = await self.model.generate_content_async(prompt)
            import json
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            # Ensure it is a list
            data = json.loads(text)
            final_data = []
            if isinstance(data, list):
                final_data = data
            elif isinstance(data, dict):
                final_data = [data]
            
            if final_data:
                # Add fallback links to recommendation items if missing (similar to generate_book_recommendations)
                for item in final_data:
                    if 'link' not in item or not item['link']:
                         import urllib.parse
                         q = f"{item.get('source_title', '')} {item.get('author', '')}".strip()
                         item['link'] = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={urllib.parse.quote(q)}"
                    if 'image' not in item:
                        item['image'] = ""

                self._cache[cache_key] = final_data
            
            return final_data
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            # Fallback to mock data on error as well
            base_mock = [
                 {
                     "content": "가장 훌륭한 시는 아직 쓰여지지 않았다.",
                     "source_title": "나짐 히크메트 시집",
                     "author": "나짐 히크메트",
                     "source_type": source_type,
                     "tags": ["희망", "시", "미래"]
                 }
            ] * pool_size
            
            # Enrich fallback
            for m in base_mock:
                 m["link"] = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={m['source_title']}"
                 m["image"] = ""
            
            return base_mock
    async def get_related_quotes(self, current_quote_content: str, limit: int = 3) -> list[dict]:
        """
        Generate quotes related to the provided quote content (Chain Recommendation).
        Infinite exploration enabled by context-aware prompting.
        """
        if not self.model:
            logger.warning("AI service not initialized. Returning empty list for related quotes.")
            return []

        prompt = f"""
        You are a creative muse. The user is reading this quote:
        "{current_quote_content}"
        
        Recommend {limit} NEW and DISTINCT quotes that are related to this one.
        They can be:
        1. Similar in theme (deepening the mood)
        2. A counter-perspective (offering a different view)
        3. From the same author or work (if famous)
        
        The goal is to let the user endlessly surf through interesting quotes.
        Target Language: Korean (Must be in Korean).
        
        Please provide the response in valid JSON format as a LIST of objects with the following keys:
        - content: The quote text (in Korean).
        - source_title: The title of the work (in Korean).
        - author: The author or character (in Korean).
        - source_type: "book" (or movie/drama if relevant).
        - tags: A list of 1-3 keywords.

        Do not include markdown formatting. Just the raw JSON list.
        """
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.9  # High temperature for variety
                }
            )
            import json
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            data = json.loads(text)
            
            # Normalize list
            if isinstance(data, dict):
                data = [data]
            
            # Add fallback links
            if data:
                 import urllib.parse
                 for item in data:
                     if 'link' not in item or not item['link']:
                          q = f"{item.get('source_title', '')} {item.get('author', '')}".strip()
                          item['link'] = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={urllib.parse.quote(q)}"
                     if 'image' not in item:
                         item['image'] = ""
            
            return data
        except Exception as e:
            logger.error(f"Error generating related quotes: {e}")
            return []
