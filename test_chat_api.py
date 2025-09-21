import requests
import json
import time

def test_chat_endpoint():
    """Test the chat endpoint to see what's failing"""

    # Test 1: Health check
    try:
        print("🔍 Testing health endpoint...")
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

    # Test 2: Chat endpoint
    try:
        print("🔍 Testing chat endpoint...")
        payload = {"message": "test query"}
        response = requests.post(
            "http://localhost:8000/chat/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("✅ Chat endpoint working")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Starting FloatChat API Tests...")
    test_chat_endpoint()
