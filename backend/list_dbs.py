from sqlalchemy import create_engine, text
import sys

# DATABASE_URL WITHOUT DB info
# Using the user provided IP and password
url = "mysql+pymysql://jinwoo:Bootcamp%232025@34.136.215.22:3306"

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        print("Connected! Listing databases:")
        result = conn.execute(text("SHOW DATABASES"))
        dbs = [row[0] for row in result]
        print(dbs)
        
        for db in ['quote_db', 'quote_collection']:
            if db in dbs:
                print(f"\nChecking tables in {db}...")
                try:
                    conn.execute(text(f"USE {db}"))
                    result = conn.execute(text("SHOW TABLES"))
                    tables = [row[0] for row in result]
                    print(tables)
                except Exception as e:
                    print(f"Error checking {db}: {e}")
except Exception as e:
    print(f"Error: {e}")
