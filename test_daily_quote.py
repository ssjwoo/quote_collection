import asyncio
import os
import sys

# Add current directory to path so we can import app modules
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from llm.ai_service import AIService
from app.core.config import settings

async def test():
    print("Initializing AIService...")
    try:
        service = AIService(
            project_id=settings.google_project_id, 
            location=settings.google_location, 
            aladin_api_key=settings.aladin_api_key
        )
        print("Service initialized. Getting daily quote...")
        res = await service.get_daily_quote('book')
        print(f"Daily Quote Result: {res}")
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
