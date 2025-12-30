import asyncio
import aiohttp
import sys

async def debug_popular():
    # Test for "book" and "movie"
    for mode in ["book", "movie"]:
        url = f"http://localhost:8081/quote/popular/today/{mode}"
        print(f"Calling {url}...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    print(f"Status: {response.status}")
                    text = await response.text()
                    print(f"Response: {text[:200]}...") # Print first 200 chars
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(debug_popular())
