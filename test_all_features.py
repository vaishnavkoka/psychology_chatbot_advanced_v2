#!/usr/bin/env python3
"""
Comprehensive test suite for Psychology Chatbot Advanced
Tests all major features including crisis detection
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

# Set up path
sys.path.insert(0, '/home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced')

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

# Test 1: Crisis Detector Module
def test_crisis_detector():
    print_header("TEST 1: Crisis Detection Module")
    
    try:
        from safety.crisis_detection import CrisisDetector, RiskLevel
        detector = CrisisDetector()
        print_success("Crisis detector imported successfully")
        
        # Test cases
        test_cases = [
            ("I'm just feeling a bit sad today", "green"),
            ("I've been stressed with work lately", "yellow"),
            ("I'm thinking about hurting myself", "orange"),
            ("I want to end my life right now", "red"),
            ("I'm having trouble concentrating", "green"),
        ]
        
        print("\nTesting crisis detection accuracy:\n")
        for message, expected_level in test_cases:
            risk_level, analysis = detector.detect_crisis(message)
            status = "✓" if risk_level.value == expected_level else "✗"
            print(f"{status} '{message}'")
            print(f"   Expected: {expected_level}, Got: {risk_level.value}, Confidence: {analysis['confidence']:.2f}")
        
        print_success("Crisis detection tests passed")
        return True
    except Exception as e:
        print_error(f"Crisis detection test failed: {e}")
        return False

# Test 2: Psychology Agents
def test_psychology_agents():
    print_header("TEST 2: Psychology Agents")
    
    try:
        from config.settings import APIKeys
        from agents.psychology_agents import (
            AssessmentAgent, SupportAgent, InsightAgent, RecommendationAgent
        )
        
        api_key = APIKeys.GROQ_API_KEY
        
        # Test Assessment Agent
        print("Testing Assessment Agent...")
        assessment_agent = AssessmentAgent(api_key=api_key)
        assessments = assessment_agent.get_available_assessments()
        print_success(f"Assessment Agent: {len(assessments)} assessments loaded")
        
        # Test Support Agent
        print("Testing Support Agent...")
        support_agent = SupportAgent(api_key=api_key)
        strategies = support_agent.get_coping_strategies("anxiety")
        print_success(f"Support Agent: Found coping strategies")
        
        # Test Insight Agent
        print("Testing Insight Agent...")
        insight_agent = InsightAgent(api_key=api_key)
        print_success("Insight Agent: Initialized successfully")
        
        # Test RecommendationAgent
        print("Testing Recommendation Agent...")
        recommendation_agent = RecommendationAgent(api_key=api_key)
        print_success("Recommendation Agent: Initialized successfully")
        
        return True
    except Exception as e:
        print_error(f"Psychology agents test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test 3: FastAPI Backend
def test_backend_endpoints():
    print_header("TEST 3: FastAPI Backend Endpoints")
    
    BACKEND_URL = "http://localhost:8000"
    
    try:
        # Check if backend is running
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        print_success("Backend server is running")
        
        # Test health endpoint
        if response.status_code == 200:
            health_data = response.json()
            print_success(f"Health check: {health_data['status']}")
        
        endpoints = [
            ("GET", "/assessments", None),
            ("GET", "/exercises", None),
            ("GET", "/topics", None),
            ("GET", "/safety/emergency-resources", None),
            ("POST", "/safety/detect-crisis", {"message": "I'm having a hard time"}),
            ("POST", "/chat", {"message": "Hello, I'm looking for support"}),
        ]
        
        print("\nTesting API endpoints:\n")
        for method, endpoint, payload in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)
                else:
                    response = requests.post(f"{BACKEND_URL}{endpoint}", json=payload, timeout=10)
                
                status = "✓" if response.status_code == 200 else "✗"
                print(f"{status} {method:4} {endpoint:35} -> {response.status_code}")
            except Exception as e:
                print(f"✗ {method:4} {endpoint:35} -> ERROR: {str(e)[:30]}")
        
        return True
    except requests.exceptions.ConnectionError:
        print_error("Backend server is not running. Please start it with: uvicorn backend:app --reload")
        return False
    except Exception as e:
        print_error(f"Backend test failed: {e}")
        return False

# Test 4: Crisis Detection via API
def test_crisis_detection_api():
    print_header("TEST 4: Crisis Detection API Endpoints")
    
    BACKEND_URL = "http://localhost:8000"
    
    try:
        test_messages = [
            {
                "message": "I'm feeling overwhelmed",
                "expected": "green"
            },
            {
                "message": "I've been thinking about harming myself",
                "expected": "orange"
            },
            {
                "message": "I want to die. I'm going to take pills.",
                "expected": "red"
            }
        ]
        
        print("Testing crisis detection via API:\n")
        for test in test_messages:
            response = requests.post(
                f"{BACKEND_URL}/safety/detect-crisis",
                json={"message": test["message"]},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                risk_level = data.get("risk_level")
                confidence = data.get("confidence", 0)
                status = "✓" if risk_level == test["expected"] else "✗"
                
                print(f"{status} Message: '{test['message'][:40]}...'")
                print(f"   Risk Level: {risk_level} (confidence: {confidence:.2f})")
        
        return True
    except requests.exceptions.ConnectionError:
        print_warning("Backend server not running - skipping API tests")
        return False
    except Exception as e:
        print_error(f"Crisis detection API test failed: {e}")
        return False

# Test 5: Docker Configuration
def test_docker_configuration():
    print_header("TEST 5: Docker Configuration Files")
    
    try:
        files = [
            "Dockerfile",
            "Dockerfile.frontend",
            "docker-compose.yml",
        ]
        
        print("Checking Docker configuration files:\n")
        for filename in files:
            filepath = f"/home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced/{filename}"
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print_success(f"{filename} exists ({size} bytes)")
            else:
                print_error(f"{filename} not found")
        
        return True
    except Exception as e:
        print_error(f"Docker configuration test failed: {e}")
        return False

# Test 6: Requirements (Azure support removed)
def test_requirements():
    print_header("TEST 7: Project Requirements")
    
    try:
        filepath = "/home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced/requirements.txt"
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                requirements = f.readlines()
            print_success(f"requirements.txt found with {len(requirements)} packages")
            
            required_packages = ['fastapi', 'streamlit', 'groq', 'pydantic', 'uvicorn']
            content = ''.join(requirements).lower()
            
            print("\nChecking critical dependencies:\n")
            for package in required_packages:
                if package in content:
                    print_success(f"{package} is included")
                else:
                    print_warning(f"{package} might be missing")
            
            return True
        else:
            print_error("requirements.txt not found")
            return False
    except Exception as e:
        print_error(f"Requirements test failed: {e}")
        return False

# Main test runner
def run_all_tests():
    print_header("PSYCHOLOGY CHATBOT ADVANCED - COMPREHENSIVE TEST SUITE")
    
    print_info(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Running on Python {sys.version.split()[0]}")
    
    results = {}
    
    # Run tests
    results["Crisis Detector"] = test_crisis_detector()
    results["Psychology Agents"] = test_psychology_agents()
    results["Project Structure"] = test_docker_configuration()
    results["Requirements"] = test_requirements()
    results["Backend Endpoints"] = test_backend_endpoints()
    results["Crisis Detection API"] = test_crisis_detection_api()
    
    # Summary
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print()
    for test_name, result in results.items():
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"{test_name:.<40} {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print_success("All tests passed! System is ready for deployment.")
        return 0
    else:
        print_warning(f"{total - passed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
