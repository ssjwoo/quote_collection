import asyncio
import aiohttp
import os
from dotenv import load_dotenv

# Load env from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

ALADIN_API_KEY = os.getenv("ALADIN_API_KEY")

async def check_aladin():
    print(f"Checking Aladin API Key: {ALADIN_API_KEY}")
    if not ALADIN_API_KEY:
        print("ERROR: ALADIN_API_KEY is missing in .env")
        return

    query = "채식주의자"
    url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx"
    params = {
        "ttbkey": ALADIN_API_KEY,
        "Query": query,
        "QueryType": "Keyword",
        "MaxResults": "1",
        "start": "1",
        "SearchTarget": "Book",
        "output": "js",
        "Version": "20131101"
    }

    print(f"Sending request to {url}...")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                try:
                    data = await response.json()
                    print(f"Response Data: {str(data)[:200]}...")
                    if "item" in data and len(data["item"]) > 0:
                        print("SUCCESS: Found book item!")
                        print(f"Image URL: {data['item'][0].get('cover')}")
                    elif "errorCode" in data:
                        print(f"ERROR: API returned error: {data.get('errorMessage')}")
                    else:
                        print("WARNING: No items found, but no error code.")
                except Exception as e:
                    print(f"ERROR: Failed to parse JSON: {e}")
                    text = await response.text()
                    print(f"Raw Response: {text[:200]}")
            else:
                print("ERROR: HTTP Status not 200")

if __name__ == "__main__":
    asyncio.run(check_aladin())
