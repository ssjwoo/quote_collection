from sqlalchemy import create_engine, text
from app.core.config import settings
import sys
import os

sys.path.append(os.getcwd())

def check_data():
    engine = create_engine(settings.sync_database_url)
    with engine.connect() as conn:
        print("--- Checking Quotes ---")
        try:
            result = conn.execute(text("SELECT id, content FROM quotes LIMIT 5"))
            rows = result.fetchall()
            if not rows:
                print("No quotes found (Table is empty).")
            else:
                for row in rows:
                    print(f"ID: {row[0]}, Content: {row[1]}")
        except Exception as e:
            print(f"Error querying quotes: {e}")

if __name__ == "__main__":
    check_data()
