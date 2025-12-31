import asyncio
import sys
import os
import logging

# Setup logging to see what vertexai/google-cloud-aiplatform is doing
logging.basicConfig(level=logging.DEBUG)

# Add paths
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../llm")))

from app.core.config import settings

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    print("Imports successful")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

async def debug_ai():
    project_id = settings.google_project_id
    location = settings.google_location
    print(f"Initializing with: Project ID='{project_id}', Location='{location}'")
    
    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel("gemini-1.5-flash")
        print("Model initialized. Testing generation...")
        response = await model.generate_content_async("Hello, repeat 'OK' if you see this.")
        print(f"Generation Successful! Response: {response.text}")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_ai())
