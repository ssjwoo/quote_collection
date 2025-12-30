from sqlalchemy import create_engine, text
from app.core.config import settings
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.getcwd())

def nuclear_reset():
    # Connect to 'mysql' system database to avoid locking ourselves out of 'quote_collection'
    # Parse the existing URL and replace database name
    base_url = settings.sync_database_url.rsplit('/', 1)[0] + '/mysql'
    
    print(f"Connecting to system DB: {base_url}")
    engine = create_engine(base_url, isolation_level="AUTOCOMMIT")
    
    with engine.connect() as conn:
        print("Dropping database quote_collection...")
        conn.execute(text("DROP DATABASE IF EXISTS quote_collection"))
        print("Creating database quote_collection...")
        conn.execute(text("CREATE DATABASE quote_collection"))
        print("Database recreated successfully.")

if __name__ == "__main__":
    nuclear_reset()
