import asyncio
import sys
import os
import logging

# Add paths
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../llm")))

# Enable logging
logging.basicConfig(level=logging.INFO)

async def test_book_mixture():
    from ai_service import AIService
    from app.core.config import settings
    
    ai = AIService(
        project_id=settings.google_project_id,
        location="us-central1",
        aladin_api_key=settings.aladin_api_key
    )
    
    print("\n--- [TEST] AI BOOK PICK Mixture (Goal: 3 Stable, 2 Fresh) ---")
    user_context = "I love Japanese mystery novels and Higashino Keigo."
    books = await ai.generate_book_recommendations(user_context=user_context)
    
    print(f"Total Received: {len(books)}")
    for i, b in enumerate(books):
        print(f"[{i+1}] {b.get('author')} - {b.get('title')}: {b.get('reason')[:50]}...")

if __name__ == "__main__":
    asyncio.run(test_book_mixture())
