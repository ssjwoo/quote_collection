import asyncio
import sys
import os

# Add paths
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../llm")))

async def test_minimal():
    from ai_service import AIService
    from app.core.config import settings
    
    ai = AIService(
        project_id=settings.google_project_id,
        location="us-central1",
        aladin_api_key=settings.aladin_api_key
    )
    
    print("\n--- Testing Generic Recommendations ---")
    recoms = await ai.get_recommendations("book", limit=3)
    print(f"Result count: {len(recoms) if recoms else 'None'}")
    if recoms:
        for r in recoms[:1]:
            print(f"Sample: {r.get('content')[:50]}...")

    print("\n--- Testing Book Recommendations ---")
    book_recoms = await ai.generate_book_recommendations("User context")
    print(f"Result count: {len(book_recoms) if book_recoms else 'None'}")

if __name__ == "__main__":
    asyncio.run(test_minimal())
