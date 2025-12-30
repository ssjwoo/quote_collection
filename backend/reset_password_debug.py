
import asyncio
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.getcwd())

from app.database import get_async_db
from app.models.user import User
from app.core.auth import hash_password
from sqlalchemy import select, update

async def reset_password(email, new_password):
    async for session in get_async_db():
        print(f"Searching for user: {email}")
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if user:
            print(f"User found: {user.email}")
            hashed = hash_password(new_password)
            user.hashed_password = hashed
            await session.commit()
            print(f"Password reset successfully for {email}")
            print(f"New password: {new_password}")
        else:
            print(f"User {email} not found!")
        break

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    email = "test@test.com"
    new_password = "test1234!"
    asyncio.run(reset_password(email, new_password))
