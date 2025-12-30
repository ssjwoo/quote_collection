from sqlalchemy_utils import drop_database, database_exists
from app.core.config import settings
import sys
import os

# Add current directory to sys.path to ensure app module is found
sys.path.append(os.getcwd())

def reset_database():
    url = settings.sync_database_url
    print(f"Target Database URL: {url}")
    
    if database_exists(url):
        print("Dropping database...")
        drop_database(url)
        print("Database dropped successfully.")
    else:
        print("Database does not exist.")

if __name__ == "__main__":
    reset_database()
