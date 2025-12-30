import requests
import json

def test_endpoint():
    print("Testing /recommendations endpoint...")
    url = "http://127.0.0.1:8081/recommendations/?source_type=book&limit=3"
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print("Raw Response Text:")
        print(response.text)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Parsed JSON (Type: {type(data)}):")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("Request failed.")
            
    except Exception as e:
        print(f"Error testing endpoint: {e}")

if __name__ == "__main__":
    test_endpoint()
