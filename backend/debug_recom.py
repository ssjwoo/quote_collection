import asyncio
import sys
import os
import logging

# Add paths
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../llm")))

# Enable logging to see the error
logging.basicConfig(level=logging.INFO)

async def debug_recommendations():
    from ai_service import AIService
    from app.core.config import settings
    
    ai = AIService(
        project_id=settings.google_project_id,
        location="us-central1",
        aladin_api_key=settings.aladin_api_key
    )
    
    print("\n--- Direct Call to _generate_json ---")
    prompt = "Recommend 1 short quote from a book in JSON format: [{\"content\": \"...\", \"source_title\": \"...\", \"author\": \"...\", \"source_type\": \"book\", \"tags\": [\"...\"]}]"
    res = await ai._generate_json(prompt)
    print(f"Result: {res}")
    
    print("\n--- Case 1: Generic Recommendations ---")
    try:
        recoms = await ai.get_recommendations("book", limit=3)
        print(f"Generic Result Count: {len(recoms) if recoms else 'None'}")
    except Exception as e:
        print(f"Generic Failed: {e}")

    print("\n--- Case 2: Book Recommendations ---")
    try:
        books = await ai.generate_book_recommendations("User interested in Kafka")
        print(f"Books Result Count: {len(books) if books else 'None'}")
    except Exception as e:
        print(f"Books Failed: {e}")

if __name__ == "__main__":
    asyncio.run(debug_recommendations())
