import asyncio
import sys
import os
import logging

# Add paths
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../llm")))

# Enable logging
logging.basicConfig(level=logging.INFO)

async def test_mixture():
    from ai_service import AIService
    from app.core.config import settings
    
    ai = AIService(
        project_id=settings.google_project_id,
        location="us-central1",
        aladin_api_key=settings.aladin_api_key
    )
    
    print("\n--- [TEST 1] Main Page Mixture (Goal: 4 Stable, 2 Fresh) ---")
    recoms = await ai.get_recommendations("book", limit=6, user_context="Modern philosophy, existentialism, Kafka")
    print(f"Total Received: {len(recoms)}")
    for i, r in enumerate(recoms):
        print(f"[{i+1}] {r.get('author')} - {r.get('source_title')}: {r.get('content')[:40]}...")

    print("\n--- [TEST 2] Related Page Mixture (Goal: 2 Stable, 1 Fresh) ---")
    current_quote = "인생은 멀리서 보면 희극이고 가까이서 보면 비극이다."
    related = await ai.get_related_quotes(current_quote, limit=3)
    print(f"Total Received: {len(related)}")
    for i, r in enumerate(related):
        print(f"[{i+1}] {r.get('author')} - {r.get('source_title')}: {r.get('content')[:40]}...")

if __name__ == "__main__":
    asyncio.run(test_mixture())
