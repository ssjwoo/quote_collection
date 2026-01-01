import requests
import json

def test_api():
    print("Testing /recommendations/ ...")
    try:
        r = requests.get("http://localhost:8081/recommendations/?source_type=book&limit=3", timeout=60)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Count: {len(data)}")
            if data:
                print(f"First item: {data[0].get('content')[:50]}...")
        else:
            print(f"Error: {r.text}")
    except Exception as e:
        print(f"Failed to connect: {e}")

    print("\nTesting /recommendations/ai ... (Requires Auth)")
    # Since we can't easily auth here without a token, let's at least check if it's reachable
    try:
        r = requests.post("http://localhost:8081/recommendations/ai", timeout=60)
        print(f"Status (should be 401/403 or 422 if no auth): {r.status_code}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_api()
