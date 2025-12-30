import asyncio
import aiohttp
import sys

async def debug_ai_recom():
    base_url = "http://localhost:8081"
    
    # 1. Login
    login_url = f"{base_url}/auth/login"
    login_data = {
        "username": "test@test.com",
        "password": "test1234!"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://localhost:5173"
    }
    
    print(f"1. Attempting login to {login_url}...")
    token = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(login_url, data=login_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    token = data.get("access_token")
                    print("   Login successful. Token obtained.")
                else:
                    print(f"   Login failed: {response.status}")
                    text = await response.text()
                    print(f"   {text}")
                    return

            # 2. Call AI Recommendations
            if token:
                ai_url = f"{base_url}/recommendations/ai"
                # The endpoint expects UserContext in body, and Auth header
                auth_headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                     "Origin": "http://localhost:5173"
                }
                # Check backend code: verify what body it expects. 
                # In previous view, it took 'user_context: str' maybe?
                # Let's assume blank body or simple json for now.
                payload = {"user_context": "I like science fiction."} 
                
                print(f"2. Calling {ai_url}...")
                async with session.post(ai_url, json=payload, headers=auth_headers) as ai_res:
                    print(f"   Status: {ai_res.status}")
                    text = await ai_res.text()
                    print(f"   Response: {text}")

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(debug_ai_recom())
