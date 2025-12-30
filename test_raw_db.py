import pymysql

def test_raw_connection():
    # Final confirmation of details
    host = "34.136.215.22"
    user = "jinwoo"
    # New complex password
    password = r"rV;p1I6<(Qu9v+*x" 
    db = "quote_collection"

    print(f"Testing raw pymysql connection to {host} as {user}...")
    
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db,
            port=3306,
            connect_timeout=10
        )
        print("Success! Raw connection established.")
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Query 'SELECT 1' successful.")
        conn.close()
    except Exception as e:
        print(f"Failed! Error: {e}")

if __name__ == "__main__":
    test_raw_connection()
