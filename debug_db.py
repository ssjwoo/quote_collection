import os
import sys
from sqlalchemy import create_engine, text

# Add backend to path to import settings
sys.path.append('backend')
from app.core.config import settings

def test_connection():
    print(f"Attempting to connect with:")
    print(f"  URL: {settings.sync_database_url}")
    
    try:
        # Create a synchronous engine for testing
        engine = create_engine(settings.sync_database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Successfully connected and executed 'SELECT 1'")
            
            # Check current user and database
            user_res = conn.execute(text("SELECT CURRENT_USER()")).scalar()
            db_res = conn.execute(text("SELECT DATABASE()")).scalar()
            print(f"  Connected as: {user_res}")
            print(f"  Database: {db_res}")
            
    except Exception as e:
        print(f"\nConnection Failed!")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        
        if "1045" in str(e):
            print("\nAdvice: Access Denied (1045). This usually means:")
            print("1. The password in .env doesn't match the one in GCP console.")
            print("2. The user doesn't have permission for the 'quote_collection' database.")
            print("3. There's a typo in the username.")

if __name__ == "__main__":
    test_connection()
