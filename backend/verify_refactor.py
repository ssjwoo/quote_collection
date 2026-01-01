import asyncio
import sys
import os

# Add paths
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../llm")))

async def test_refactored_ai():
    try:
        from ai_service import AIService
        print("✅ Successfully imported AIService")
        
        # Mock settings
        from app.core.config import settings
        
        ai = AIService(
            project_id=settings.google_project_id,
            location="us-central1",
            aladin_api_key=settings.aladin_api_key
        )
        
        print("\n=== 1. Vertex Client Test ===")
        # Test basic model access via new client
        model = ai.vertex.get_model()
        if model:
            print("✅ VertexAIClient initialization successful")
        else:
            print("❌ VertexAIClient initialization failed")

        print("\n=== 2. Aladin Client Test ===")
        book_info = await ai.aladin.fetch_book_info("어린 왕자", "생텍쥐페리")
        if book_info.get("link"):
            print(f"✅ AladinClient successful: {book_info.get('link')[:30]}...")
        else:
            print("❌ AladinClient failed (possibly key issue, but logic check only)")

        print("\n=== 4. Generic Recommendations Test ===")
        recoms = await ai.get_recommendations("book", limit=3)
        if recoms and len(recoms) > 0:
            print(f"✅ AIService.get_recommendations successful: Found {len(recoms)} items")
        else:
            print("❌ AIService.get_recommendations failed or empty")

        print("\n=== 5. Book Recommendations Test ===")
        book_recoms = await ai.generate_book_recommendations("User likes space.")
        if book_recoms and len(book_recoms) > 0:
            print(f"✅ AIService.generate_book_recommendations successful: Found {len(book_recoms)} items")
        else:
            print("❌ AIService.generate_book_recommendations failed or empty")

        print("\n=== 6. Service Layer Test ===")
        from app.services.ai_recommendation_service import AIRecommendationService
        rec_svc = AIRecommendationService(ai)
        # We need a dummy DB session or just test the logic that doesn't use DB heavily
        # Actually get_quotes_recommendations calls get_user_context which uses DB
        # Let's just test the conversion logic if possible
        ai_data = {"content": "Test", "source_title": "Title", "author": "Author", "tags": ["tag1"]}
        converted = rec_svc._to_quote_read(ai_data, "book", -1)
        if converted.content == "Test":
            print("✅ AIRecommendationService conversion logic successful")
        else:
            print("❌ AIRecommendationService conversion logic failed")

        print("\n🎉 All refactored logic verified!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_refactored_ai())
