import asyncio
import sys
import os
from app.core.config import settings

# Add backend directory to sys.path
sys.path.append(os.getcwd())

# Mock AIService import
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../llm")))
    from ai_service import AIService
except ImportError:
    print("Failed to import AIService")
    sys.exit(1)

async def test_ai():
    print("Initializing AIService...")
    ai = AIService(project_id=settings.google_project_id, location=settings.google_location)
    
    print("\n--- Testing get_daily_quote ---")
    daily = await ai.get_daily_quote("book")
    print(f"Daily Quote Result: {daily}")
    
    print("\n--- Testing get_recommendations ---")
    recs = await ai.get_recommendations("book", 3)
    print(f"Recommendations Result (Type: {type(recs)}):")
    for r in recs:
        print(r)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_ai())
