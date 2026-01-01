import asyncio
import sys
import os
import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

# Add paths
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../llm")))

async def test_user_model():
    load_dotenv()
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    location = "us-central1"
    
    print(f"Testing model: gemini-2.0-flash in {project_id}/{location}")
    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel("gemini-2.0-flash")
        response = await model.generate_content_async("Hello")
        print(f"Success! Response: {response.text[:50]}...")
    except Exception as e:
        print(f"Failed with gemini-2.0-flash: {e}")

if __name__ == "__main__":
    asyncio.run(test_user_model())
