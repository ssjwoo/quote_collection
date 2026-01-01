from datetime import datetime

BOOK_RECOMMENDATION_PROMPT = """
You are a smart AI book curator. Recommend 5 books based on the user's interests and current weather in Seoul, Korea.
IMPORTANT: Provide UNIQUE, FRESH, and VARIED recommendations. Avoid repeating the same bestsellers.

MIXTURE RATIO (Crucial for 5 recommendations):
- 3 out of 5 books: Must STICK to the User's Interest/Context (STABLE).
- 2 out of 5 books: Must be from TOTALLY DIFFERENT genres or authors (FRESH/EXPLORATORY) to prevent boredom.

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

DAILY_QUOTE_PROMPT = """
Recommend a famous and inspiring quote from a {source_type} for today ({today}).
The quote must be suitable for a general audience and widely recognized.

Please provide the response in valid JSON format with the following keys:
- content: The quote text (in Korean).
- source_title: The title of the {source_type} (in Korean).
- author: The author or character who said it (in Korean).
- source_type: "{source_type}"
- tags: A list of 1-3 keywords relevant to the quote (in Korean).

Do not include markdown formatting. Just the raw JSON string.
"""

GENERIC_RECOMMENDATION_PROMPT = """
Recommend {pool_size} POWERFUL and AUTHENTIC quotes exclusively from EXISTING BOOKS (Literature, Philosophy, History).

CRITICAL RULES:
1. NO PROVERBS, NO GENERAL SAYINGS, NO ANONYMOUS ADAGES.
2. EVERY quote MUST have a SPECIFIC and REAL BOOK TITLE and a KNOWN AUTHOR.
3. MIXTURE RATIO (Crucial):
   - 4 out of 6 quotes: Must STICK to the User's Interest/Context (STABLE).
   - 2 out of 6 quotes: Must be from TOTALLY DIFFERENT genres or authors (FRESH/EXPLORATORY) to prevent boredom.
4. AVOID cliché or overly common sayings. Seek for deep, artistic sentences.

User's Interest/Context:
{user_context}
Only Korean.

Response in valid JSON format LIST of objects:
- content: The quote text (in Korean).
- source_title: The title of the work (in Korean).
- author: The author or character who said it (in Korean).
- source_type: "{source_type}"
- tags: A list of 1-3 keywords.

Just the raw JSON list.
"""

RELATED_QUOTE_PROMPT = """
You are a creative muse. The user is reading this quote:
"{current_quote_content}"

Recommend {limit} NEW and DISTINCT quotes derived EXCLUSIVELY from REAL BOOKS or WORKS.

MIXTURE RULES (For 3 recommendations):
- 2 quotes: High relevance to the current quote's theme/mood (STABLE).
- 1 quote: A fresh perspective or a contrasting but interesting genre (FRESH).

Each recommendation MUST include a verified Book Title and Author.
Target Language: Korean.

Response in valid JSON format LIST:
- content: The quote text (in Korean).
- source_title: The title of the work (in Korean).
- author: The author or character (in Korean).
- source_type: "book"
- tags: A list of 1-3 keywords.
"""
