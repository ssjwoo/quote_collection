import requests
import json

def test():
    url = "http://localhost:8081/recommendations/related"
    payload = {
        "current_quote_content": "어린왕자, 만일 네가 오후 4시에 온다면 나는 3시부터 행복해질 거야."
    }
    
    print(f"Testing endpoint: {url}")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text}")
        if response.status_code == 200:
            data = response.json()
            print("Response Data Items:")
            for item in data:
                print(f"- {item['content']} ({item['source']['title']})")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test()
