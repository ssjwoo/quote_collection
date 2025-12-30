from sqlalchemy import create_engine, text
from app.core.config import settings
import sys
import os

sys.path.append(os.getcwd())

def check_user():
    # settings.sync_database_url should now point to quote_collection on .22
    print(f"Connecting to: {settings.sync_database_url}")
    engine = create_engine(settings.sync_database_url)
    with engine.connect() as conn:
        try:
            result = conn.execute(text("SELECT id, email, hashed_password FROM users WHERE email = 'test@test.com'"))
            user = result.fetchone()
            if user:
                print(f"User found: ID={user[0]}, Email={user[1]}")
                print(f"Has password hash: {bool(user[2])}")
            else:
                print("User test@test.com NOT found in database.")
                
                # List all users just in case
                print("\nListing all users:")
                all_users = conn.execute(text("SELECT email FROM users"))
                for u in all_users:
                    print(f"- {u[0]}")
        except Exception as e:
            print(f"Error checking user: {e}")

if __name__ == "__main__":
    check_user()
