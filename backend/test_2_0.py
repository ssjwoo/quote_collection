import os
import asyncio
import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

load_dotenv()

async def test_2_0():
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    location = os.getenv("GOOGLE_LOCATION", "us-central1")
    
    print(f"Initializing Vertex AI: {project_id} in {location}")
    vertexai.init(project=project_id, location=location)
    
    model = GenerativeModel("gemini-2.0-flash-exp")
    prompt = "Give me one short inspirational quote in Korean. Return only JSON: {\"quote\": \"...\"}"
    
    print("Generating content...")
    try:
        response = await model.generate_content_async(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        print("Response received:")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_2_0())
