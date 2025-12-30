import asyncio
import aiohttp
import sys

async def debug_login():
    url = "http://localhost:8081/auth/login"
    data = {
        "username": "test@test.com",
        "password": "test1234!"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://localhost:5173"
    }
    
    print(f"Attempting login to {url}...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                status = response.status
                text = await response.text()
                print(f"Status Code: {status}")
                print(f"Response Body: {text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(debug_login())
