import asyncio
import sys
import os

sys.path.append(os.getcwd())

from app.database import AsyncSessionLocal
from sqlalchemy import text

async def check_async_data():
    async with AsyncSessionLocal() as session:
        print("--- Checking Quotes (Async) ---")
        try:
            result = await session.execute(text("SELECT id, content FROM quotes LIMIT 5"))
            rows = result.fetchall()
            if not rows:
                print("No quotes found (Async Table is empty).")
            else:
                for row in rows:
                    print(f"ID: {row[0]}, Content: {row[1]}")
        except Exception as e:
            print(f"Error checking async DB: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(check_async_data())
