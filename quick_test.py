import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("\n" + "="*60)
print("🧪 PSYCHOLOGY CHATBOT - LOCAL TESTING")
print("="*60)

# Test 1: Backend Health
print("\n[1/8] Testing Backend Health...")
try:
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    if r.status_code == 200:
        data = r.json()
        print(f"    ✅ Backend healthy: {data['status']}")
        print(f"    ✅ All agents ready: {all(data['agents_ready'].values())}")
    else:
        print(f"    ❌ Backend error: {r.status_code}")
except Exception as e:
    print(f"    ❌ Connection failed: {e}")

# Test 2: Get Assessments
print("\n[2/8] Testing GET /assessments...")
try:
    r = requests.get(f"{BASE_URL}/assessments", timeout=5)
    if r.status_code == 200:
        data = r.json()
        print(f"    ✅ Retrieved {len(data.get('assessments', []))} assessments")
    else:
        print(f"    ❌ Error: {r.status_code}")
except Exception as e:
    print(f"    ❌ Failed: {e}")

# Test 3: Get Exercises
print("\n[3/8] Testing GET /exercises...")
try:
    r = requests.get(f"{BASE_URL}/exercises", timeout=5)
    if r.status_code == 200:
        data = r.json()
        print(f"    ✅ Retrieved {len(data.get('exercises', []))} exercises")
    else:
        print(f"    ❌ Error: {r.status_code}")
except Exception as e:
    print(f"    ❌ Failed: {e}")

# Test 4: Get Topics
print("\n[4/8] Testing GET /topics...")
try:
    r = requests.get(f"{BASE_URL}/topics", timeout=5)
    if r.status_code == 200:
        data = r.json()
        print(f"    ✅ Retrieved {len(data.get('topics', []))} topics")
    else:
        print(f"    ❌ Error: {r.status_code}")
except Exception as e:
    print(f"    ❌ Failed: {e}")

# Test 5: Crisis Detection - Normal Message
print("\n[5/8] Testing POST /safety/detect-crisis (normal message)...")
try:
    payload = {"message": "I'm feeling a bit stressed about work today"}
    r = requests.post(f"{BASE_URL}/safety/detect-crisis", json=payload, timeout=5)
    if r.status_code == 200:
        data = r.json()
        risk = data.get('risk_level', 'unknown')
        conf = data.get('confidence', 0)
        print(f"    ✅ Risk Level: {risk} (Confidence: {conf:.2f})")
    else:
        print(f"    ❌ Error: {r.status_code}")
except Exception as e:
    print(f"    ❌ Failed: {e}")

# Test 6: Crisis Detection - Critical Message
print("\n[6/8] Testing POST /safety/detect-crisis (crisis message)...")
try:
    payload = {"message": "I want to end my life, I'm in too much pain"}
    r = requests.post(f"{BASE_URL}/safety/detect-crisis", json=payload, timeout=5)
    if r.status_code == 200:
        data = r.json()
        risk = data.get('risk_level', 'unknown')
        conf = data.get('confidence', 0)
        print(f"    ✅ Risk Level: {risk} (Confidence: {conf:.2f})")
        if risk in ['orange', 'red']:
            print(f"    ✅ Crisis detection working!")
    else:
        print(f"    ❌ Error: {r.status_code}")
except Exception as e:
    print(f"    ❌ Failed: {e}")

# Test 7: Emergency Resources
print("\n[7/8] Testing GET /safety/emergency-resources...")
try:
    r = requests.get(f"{BASE_URL}/safety/emergency-resources", timeout=5)
    if r.status_code == 200:
        data = r.json()
        resources = data.get('resources', {})
        print(f"    ✅ Emergency resources available")
        print(f"    ✅ Countries covered: {', '.join(list(resources.keys())[:3])}...")
    else:
        print(f"    ❌ Error: {r.status_code}")
except Exception as e:
    print(f"    ❌ Failed: {e}")

# Test 8: Chat Endpoint - Fixed
print("\n[8/8] Testing POST /chat...")
try:
    payload = {"message": "How can I manage my anxiety?"}  # Removed context
    r = requests.post(f"{BASE_URL}/chat", json=payload, timeout=10)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        has_msg = 'message' in data
        has_crisis = 'crisis_detected' in data
        print(f"    ✅ Chat response received")
        print(f"    ✅ Has message: {has_msg}")
        print(f"    ✅ Crisis detection integrated: {has_crisis}")
    else:
        print(f"    ❌ Error {r.status_code}: {r.text[:100]}")
except Exception as e:
    print(f"    ❌ Failed: {e}")

# Summary
print("\n" + "="*60)
print("✅ LOCAL TESTING SUITE COMPLETED")
print("="*60)
print("\n📍 ACCESS YOUR APPLICATION:")
print("   🎯 Frontend: http://localhost:8501")
print("   🔧 Backend Docs: http://localhost:8000/docs")  
print("   🏥 Backend API: http://localhost:8000")
print("\n")

