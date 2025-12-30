import logging
import os
import sys

logger = logging.getLogger(__name__)

# Track if libraries are functional
_VERTEX_LIBS_READY = None 

def _ensure_vertex_libs():
    global _VERTEX_LIBS_READY
    if _VERTEX_LIBS_READY is not None:
        return _VERTEX_LIBS_READY
    
    try:
        # Aggressive masking of torch before any vertexai import
        if "torch" not in sys.modules:
            from unittest.mock import MagicMock
            for mod in ["torch", "torch.cuda", "torch.distributed", "torch.nn"]:
                sys.modules[mod] = MagicMock()
        
        import vertexai
        from vertexai.generative_models import GenerativeModel, Tool
        try:
            from vertexai.generative_models import grounding
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
        self.location = location
        self.aladin_api_key = aladin_api_key or os.getenv("ALADIN_API_KEY", "")
        self._model = None
        self._cache = {}
        
    @property
    def model(self):
        if self._model:
            return self._model
        
        libs = _ensure_vertex_libs()
        if not libs:
            return None
        
        vertexai, GenerativeModel, _, _ = libs
        try:
            vertexai.init(project=self.project_id, location=self.location)
            self._model = GenerativeModel("gemini-2.0-flash")
            return self._model
        except Exception as e:
            logger.error(f"Vertex AI Init failed: {e}")
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
                            # Use larger image if available (Aladin API often gives tiny thumbs)
                            if result["image"] and "sum.jpg" in result["image"]:
                                result["image"] = result["image"].replace("sum.jpg", "cover500.jpg")
                            elif result["image"] and "ssum.jpg" in result["image"]:
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

    async def generate_book_recommendations(self, user_context: str) -> str:
        libs = _ensure_vertex_libs()
        if not libs or not self.model:
             return "AI 서비스가 초기화되지 않아 추천을 생성할 수 없습니다."
        
        _, GenerativeModel, Tool, grounding = libs

        try:
            # Define Tool for Google Search Grounding
            if grounding:
                tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
            else:
                tool = None
        except Exception as e:
            logger.warning(f"GoogleSearchRetrieval not available: {e}. Proceeding without grounding.")
            tool = None

        prompt = f"""
        You are a smart AI book curator. Recommend 5 books based on the user's interests and current weather in Seoul, Korea.
        
        Step 1: Check current weather in Seoul, Korea.
        Step 2: Select 5 books that match the weather mood and user's interests.
        
        For each book, provide:
        - "title": Exact Korean book title (한글 제목)
        - "author": Author name (저자명)
        - "reason": Short explanation why this book is interesting/recommended. 
          IMPORTANT: DO NOT MENTION THE WEATHER OR MOOD EXPLICITLY IN THE REASON. 
          The reason should be about the book's content or vibe only.
        
        User's Interest Context:
        {user_context}
        
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
            generate_kwargs = {"generation_config": {"response_mime_type": "application/json"}}
            if tool:
                generate_kwargs["tools"] = [tool]
                
            response = await self.model.generate_content_async(
                prompt,
                **generate_kwargs
            )
            
            # Clean up response text
            text = response.text.strip()
            
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            # Robust extraction: find the first '[' and last ']'
            start_index = text.find('[')
            end_index = text.rfind(']')
            
            if start_index != -1 and end_index != -1 and end_index > start_index:
                text = text[start_index : end_index + 1]
            else:
                # If no list found, log warning and return text (will fallback to plain text UI)
                logger.warning(f"Could not find JSON list in response: {text[:100]}...")
            
            # Parse JSON and add Aladin links
            import json
            from urllib.parse import quote as url_quote
            try:
                books = json.loads(text)
                
                # Fetch Aladin info for each book
                for book in books:
                    title = book.get('title', '')
                    author = book.get('author', '')
                    
                    # Try to get real book info from Aladin API
                    aladin_info = await self._fetch_aladin_book_info(title, author)
                    
                    if aladin_info["link"]:
                        book['link'] = aladin_info["link"]
                    else:
                        # Fallback to search URL
                        search_query = f"{title} {author}".strip()
                        book['link'] = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={url_quote(search_query)}"
                    
                    book['image'] = aladin_info["image"]
                    
                return json.dumps(books, ensure_ascii=False)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON, returning raw text")
                return text
            
        except Exception as e:
            logger.error(f"Error generating content from Vertex AI: {e}")
            # Return a fallback JSON error message or empty list so frontend doesn't crash
            return '[{"title": "Error", "author": "System", "reason": "AI 추천을 불러오는 중 오류가 발생했습니다.", "link": "#", "image": ""}]'

    async def get_daily_quote(self, source_type: str) -> dict:
        if not self.model:
            print("DEBUG: AI Service not available (Library/Initialization failed).")
            return None

        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        cache_key = ("daily_quote", source_type, today)

        # Initialize cache if missing (safety check)
        if not hasattr(self, '_cache'):
            self._cache = {}

        if cache_key in self._cache:
            return self._cache[cache_key]

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
            # Remove markdown if present
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            # Robust extraction for daily quote
            start_index = text.find('{')
            end_index = text.rfind('}')
            if start_index != -1 and end_index != -1:
                text = text[start_index : end_index + 1]
                
            result = json.loads(text)
            self._cache[cache_key] = result
            return result
        except Exception as e:
            logger.error(f"Error generating daily quote: {e}")
            print(f"DEBUG: Error generating daily quote: {e}")
            return None

    async def get_recommendations(self, source_type: str, limit: int = 3) -> list[dict]:
        if not self.model:
            return []

        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        cache_key = ("recommendations", source_type, limit, today)

        # Initialize cache if missing (safety check)
        if not hasattr(self, '_cache'):
            self._cache = {}

        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = f"""
        Recommend {limit} famous and inspiring quotes from different {source_type}s for today ({today}).
        
        The quotes must be suitable for a general audience and widely recognized. Only Korean.
        
        Please provide the response in valid JSON format as a LIST of objects with the following keys:
        - content: The quote text (in Korean).
        - source_title: The title of the {source_type} (in Korean).
        - author: The author or character who said it (in Korean).
        - source_type: "{source_type}"
        - tags: A list of 1-3 keywords relevant to the quote (in Korean).

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
                self._cache[cache_key] = final_data
            
            return final_data
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []
