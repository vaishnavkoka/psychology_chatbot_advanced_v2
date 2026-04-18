import requests
import json

BASE_URL = "http://localhost:8000"

# Test chat with different payloads
payloads = [
    {"message": "How can I manage my anxiety?", "context": {}},
    {"message": "How can I manage my anxiety?", "context": None},
    {"message": "How can I manage my anxiety?"},
]

for i, payload in enumerate(payloads):
    print(f"\n[Test {i+1}] Payload: {json.dumps(payload)}")
    try:
        r = requests.post(f"{BASE_URL}/chat", json=payload, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"✅ Response received")
            print(f"Message: {data.get('message', '')[:100]}...")
        else:
            print(f"❌ Error: {r.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
