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
             logger.warning("AI service not initialized or model failed. Using Dynamic Fallback Data.")
             # Fallback: Instead of fixed 5 books, use a slightly larger pool or try to fetch some random titles?
             # For now, let's at least avoid the same 5 every time if possible.
             # But without AI, we are limited. Let's provide a larger list and sample from it.
             dynamic_fallback = [
                 {"title": "달러구트 꿈 백화점", "author": "이미예", "reason": "힐링과 감동을 주는 한국형 판타지 소설"},
                 {"title": "불편한 편의점", "author": "김호연", "reason": "따뜻한 위로가 필요한 당신에게 추천하는 베스트셀러"},
                 {"title": "채식주의자", "author": "한강", "reason": "강렬한 문체와 깊이 있는 주제의식의 맨부커상 수상작"},
                 {"title": "모순", "author": "양귀자", "reason": "인생의 모순을 날카롭지만 따뜻하게 그려낸 수작"},
                 {"title": "파친코", "author": "이민진", "reason": "역사의 흐름 속에서 피어난 강인한 생명력의 이야기"},
                 {"title": "지구 끝의 온기", "author": "김초엽", "reason": "SF의 상상력과 따뜻한 휴머니즘이 만난 소설"},
                 {"title": "소년이 온다", "author": "한강", "reason": "역사의 아픔을 섬세하고 강렬한 필치로 그려낸 작품"},
                 {"title": "아몬드", "author": "손원평", "reason": "감정을 느끼지 못하는 소년의 특별한 성장 이야기"},
                 {"title": "미드나잇 라이브러리", "author": "매트 헤이그", "reason": "살아보지 못한 수많은 삶들을 경험하는 판타지 여행"}
             ]
             import random
             sampled_fallback = random.sample(dynamic_fallback, min(5, len(dynamic_fallback)))
             
             try:
                 for book in sampled_fallback:
                    title = book.get('title', '')
                    author = book.get('author', '')
                    aladin_info = await self._fetch_aladin_book_info(title, author)
                    book['link'] = aladin_info.get("link") or f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={title}"
                    book['image'] = aladin_info.get("image", "")
                 
                 return sampled_fallback
             except Exception as e:
                 logger.error(f"Error processing fallback data: {e}")
                 return []
        
        _, GenerativeModel, Tool, grounding = libs

        try:
            if grounding:
                tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
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
             logger.warning(f"AI service not initialized. Returning mock recommendations for {source_type}")
             # Mock data needs to be diverse enough if we want to test randomization, but keeping simple for now
             # Mock data needs to be diverse enough if we want to test randomization
             base_mock = [
                 {"content": "사람은 무엇으로 사는가? 사랑으로 산다.", "source_title": "사람은 무엇으로 사는가", "author": "톨스토이", "source_type": source_type, "tags": ["사랑", "인생", "고전"]},
                 {"content": "행복한 가정은 모두 엇비슷하고 불행한 가정은 불행한 이유가 제각기 다르다.", "source_title": "안나 카레니나", "author": "톨스토이", "source_type": source_type, "tags": ["행복", "가정", "첫문장"]},
                 {"content": "내일은 내일의 태양이 뜬다.", "source_title": "바람과 함께 사라지다", "author": "마가렛 미첼", "source_type": source_type, "tags": ["희망", "내일", "고전"]},
                 {"content": "삶이 그대를 속일지라도 슬퍼하거나 노여워하지 말라.", "source_title": "삶이 그대를 속일지라도", "author": "푸시킨", "source_type": source_type, "tags": ["삶", "위로", "희망"]},
                 {"content": "별을 노래하는 마음으로 모든 죽어가는 것을 사랑해야지.", "source_title": "서시", "author": "윤동주", "source_type": source_type, "tags": ["별", "사랑", "서정"]},
                 {"content": "죽는 날까지 하늘을 우러러 한 점 부끄럼이 없기를.", "source_title": "서시", "author": "윤동주", "source_type": source_type, "tags": ["성찰", "부끄러움", "하늘"]},
                 {"content": "자세히 보아야 예쁘다. 오래 보아야 사랑스럽다. 너도 그렇다.", "source_title": "풀꽃", "author": "나태주", "source_type": source_type, "tags": ["사랑", "위로", "풀꽃"]},
                 {"content": "가장 훌륭한 시는 아직 쓰여지지 않았다.", "source_title": "진정한 여행", "author": "나짐 히크메트", "source_type": source_type, "tags": ["희망", "미래", "시"]},
                 {"content": "너의 우울이 길다. 후회가, 체념이, 무기력이 너무 길다.", "source_title": "나의 우울이 길다", "author": "기형도", "source_type": source_type, "tags": ["우울", "성찰", "시간"]},
                 {"content": "지나간 것은 지나간 대로 그런 의미가 있죠.", "source_title": "걱정말아요 그대", "author": "전인권", "source_type": source_type, "tags": ["위로", "과거", "음악"]},
                 {"content": "어린왕자, 만일 네가 오후 4시에 온다면 나는 3시부터 행복해질 거야.", "source_title": "어린왕자", "author": "생텍쥐페리", "source_type": source_type, "tags": ["행복", "기다림", "순수"]},
                 {"content": "중요한 것은 눈에 보이지 않아. 마음으로 보아야 잘 보여.", "source_title": "어린왕자", "author": "생텍쥐페리", "source_type": source_type, "tags": ["본질", "마음", "진실"]},
                 {"content": "너의 장미꽃이 그토록 소중한 것은 그 꽃을 위해 네가 공들인 그 시간 때문이야.", "source_title": "어린왕자", "author": "생텍쥐페리", "source_type": source_type, "tags": ["관계", "노력", "사랑"]},
                 {"content": "건강한 신체에 건전한 정신이 깃든다.", "source_title": "풍자시", "author": "유베날리스", "source_type": source_type, "tags": ["건강", "정신", "격언"]},
                 {"content": "너 자신을 알라.", "source_title": "소크라테스의 변명", "author": "소크라테스", "source_type": source_type, "tags": ["지혜", "철학", "성찰"]},
                 {"content": "인생은 멀리서 보면 희극이고 가까이서 보면 비극이다.", "source_title": "명언집", "author": "찰리 채플린", "source_type": source_type, "tags": ["인생", "희극", "비극"]},
                 {"content": "결코 포기하지 마십시오. 위대한 일은 시간이 걸립니다.", "source_title": "명언집", "author": "윈스턴 처칠", "source_type": source_type, "tags": ["끈기", "성공", "도전"]},
                 {"content": "변화하고 싶다면 지금 당장 시작하라.", "source_title": "명언집", "author": "데일 카네기", "source_type": source_type, "tags": ["변화", "실천", "시작"]},
                 {"content": "시간은 금이다.", "source_title": "격언", "author": "벤자민 프랭클린", "source_type": source_type, "tags": ["시간", "가치", "노력"]},
                 {"content": "실패는 성공의 어머니.", "source_title": "격언", "author": "에디슨", "source_type": source_type, "tags": ["실패", "성공", "교훈"]},
                 {"content": "천재는 1%의 영감과 99%의 노력으로 만들어진다.", "source_title": "격언", "author": "에디슨", "source_type": source_type, "tags": ["노력", "천재", "끈기"]},
                 {"content": "꿈을 꿀 수 있다면, 그것을 이룰 수 있다.", "source_title": "명언집", "author": "월트 디즈니", "source_type": source_type, "tags": ["꿈", "희망", "가능성"]},
                 {"content": "상상력은 지식보다 중요하다.", "source_title": "명언집", "author": "아인슈타인", "source_type": source_type, "tags": ["상상력", "지식", "창의성"]},
                 {"content": "멈추지 않는 한, 얼마나 천천히 가는지는 중요하지 않다.", "source_title": "논어", "author": "공자", "source_type": source_type, "tags": ["끈기", "속도", "지속"]},
                 {"content": "배우고 때때로 익히면 또한 기쁘지 아니한가.", "source_title": "논어", "author": "공자", "source_type": source_type, "tags": ["배움", "기쁨", "성장"]},
                 {"content": "말 한마디로 천냥 빚을 갚는다.", "source_title": "속담", "author": "한국 속담", "source_type": source_type, "tags": ["말", "지혜", "관계"]},
                 {"content": "가는 말이 고와야 오는 말이 곱다.", "source_title": "속담", "author": "한국 속담", "source_type": source_type, "tags": ["예절", "소통", "관계"]},
                 {"content": "티끌 모아 태산.", "source_title": "속담", "author": "한국 속담", "source_type": source_type, "tags": ["노력", "저축", "성실"]},
                 {"content": "피할 수 없으면 즐겨라.", "source_title": "명언집", "author": "로버트 엘리엇", "source_type": source_type, "tags": ["태도", "긍정", "인생"]},
                 {"content": "이 또한 지나가리라.", "source_title": "명언집", "author": "솔로몬의 반지", "source_type": source_type, "tags": ["위로", "시간", "인내"]}
             ]
             
             # Enrich with fallback links
             for m in base_mock:
                 m["link"] = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={m['source_title']}"
                 m["image"] = ""

             # Return distinct items
             return base_mock

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
            logger.warning("AI service not initialized. Returning standard quotes.")
            return [
                 {
                     "content": "가장 훌륭한 시는 아직 쓰여지지 않았다.",
                     "source_title": "진정한 여행",
                     "author": "나짐 히크메트",
                     "source_type": "book",
                     "tags": ["희망", "미래"]
                 },
                 {
                     "content": "중요한 것은 눈에 보이지 않아. 마음으로 보아야 잘 보여.",
                     "source_title": "어린왕자",
                     "author": "생텍쥐페리",
                     "source_type": "book",
                     "tags": ["본질", "진실"]
                 },
                 {
                     "content": "별을 노래하는 마음으로 모든 죽어가는 것을 사랑해야지.",
                     "source_title": "서시",
                     "author": "윤동주",
                     "source_type": "book",
                     "tags": ["사랑", "서정"]
                 }
            ][:limit]

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
