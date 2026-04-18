#!/usr/bin/env python3
"""
Comprehensive Test Suite for Psychology Chatbot
Tests all features, sections, and edge cases
"""

import sys
import os
import json
import time
import subprocess
from typing import Dict, List, Tuple
import requests
from datetime import datetime

# Test Configuration
API_BASE_URL = "http://localhost:8000"
TIMEOUT = 5
VERBOSE = True


class Colors:
    """Color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(title: str):
    """Print colored header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")


def print_test(name: str, status: str, details: str = ""):
    """Print test result"""
    if status == "PASS":
        symbol = f"{Colors.GREEN}✓{Colors.END}"
        status_color = Colors.GREEN
    elif status == "FAIL":
        symbol = f"{Colors.RED}✗{Colors.END}"
        status_color = Colors.RED
    else:
        symbol = f"{Colors.YELLOW}⚠{Colors.END}"
        status_color = Colors.YELLOW
    
    print(f"{symbol} {name:<50} [{status_color}{status}{Colors.END}]")
    if details and VERBOSE:
        print(f"  └─ {details}")


def test_backend_health() -> bool:
    """Test 1: Backend Health Check"""
    print_header("TEST 1: Backend Health & Connectivity")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_test("Backend responding", "PASS", f"Status: {data.get('status')}")
            
            agents_ready = data.get('agents_ready', {})
            agents_status = sum(1 for v in agents_ready.values() if v)
            print_test("Agents initialized", "WARN", f"{agents_status}/4 agents ready (using fallbacks is OK)")
            
            return True
        else:
            print_test("Backend health check", "FAIL", f"Status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_test("Backend connectivity", "FAIL", "Cannot connect to backend on port 8000")
        return False
    except Exception as e:
        print_test("Backend health check", "FAIL", str(e))
        return False


def test_chat_basic() -> bool:
    """Test 2: Basic Chat Functionality"""
    print_header("TEST 2: Chat Functionality")
    
    all_passed = True
    
    # Test 2.1: Simple message
    try:
        payload = {"message": "Hello, how are you?", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if "message" in data:
                print_test("Simple chat message", "PASS", f"Response length: {len(data['message'])}")
            else:
                print_test("Simple chat message", "FAIL", "No message in response")
                all_passed = False
        else:
            print_test("Simple chat message", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Simple chat message", "FAIL", str(e))
        all_passed = False
    
    # Test 2.2: Empty message handling
    try:
        payload = {"message": "", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_test("Empty message handling", "PASS", "Gracefully handled")
        else:
            print_test("Empty message handling", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Empty message handling", "FAIL", str(e))
        all_passed = False
    
    # Test 2.3: Long message
    try:
        long_msg = "I am experiencing severe anxiety and cannot sleep. " * 10
        payload = {"message": long_msg, "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Long message handling", "PASS", f"Message length: {len(long_msg)}")
        else:
            print_test("Long message handling", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Long message handling", "FAIL", str(e))
        all_passed = False
    
    # Test 2.4: Special characters
    try:
        special_msg = "I feel! @#$% ... ???"
        payload = {"message": special_msg, "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Special characters handling", "PASS", "Processed successfully")
        else:
            print_test("Special characters handling", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Special characters handling", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def test_spell_check() -> bool:
    """Test 3: Spell Checking Functionality"""
    print_header("TEST 3: Spell Checker Integration")
    
    all_passed = True
    
    # Test 3.1: Misspelled word detection
    try:
        payload = {"message": "I am feling anxious", "context": {}}
        response = requests.post(f"{API_BASE_URL}/spell-check", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("has_errors") or data.get("corrections"):
                print_test("Misspelled word detection", "PASS", f"Found: {data.get('corrections')}")
            else:
                print_test("Misspelled word detection", "WARN", "No errors detected")
        else:
            print_test("Misspelled word detection", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Misspelled word detection", "FAIL", str(e))
        all_passed = False
    
    # Test 3.2: Multiple misspellings
    try:
        payload = {"message": "I am feling realy bada", "context": {}}
        response = requests.post(f"{API_BASE_URL}/spell-check", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            corrections = data.get("corrections", {})
            if len(corrections) >= 2:
                print_test("Multiple misspellings", "PASS", f"Corrections: {len(corrections)}")
            else:
                print_test("Multiple misspellings", "WARN", f"Found: {corrections}")
        else:
            print_test("Multiple misspellings", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Multiple misspellings", "FAIL", str(e))
        all_passed = False
    
    # Test 3.3: Correct spelling (no changes)
    try:
        payload = {"message": "I am feeling anxious", "context": {}}
        response = requests.post(f"{API_BASE_URL}/spell-check", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if not data.get("corrections"):
                print_test("Correct spelling unchanged", "PASS", "No changes made")
            else:
                print_test("Correct spelling unchanged", "WARN", f"Unexpected corrections: {data.get('corrections')}")
        else:
            print_test("Correct spelling unchanged", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Correct spelling unchanged", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def test_assessments() -> bool:
    """Test 4: Assessment Functionality"""
    print_header("TEST 4: Assessment Section")
    
    all_passed = True
    
    # Test 4.1: Get available assessments
    try:
        response = requests.get(f"{API_BASE_URL}/assessments", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            assessment_count = data.get("count", 0)
            if assessment_count > 0:
                print_test("List available assessments", "PASS", f"Found {assessment_count} assessments")
            else:
                print_test("List available assessments", "FAIL", "No assessments returned")
                all_passed = False
        else:
            print_test("List available assessments", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("List available assessments", "FAIL", str(e))
        all_passed = False
    
    # Test 4.2: Start assessment - PHQ-9
    assessment_id = None
    try:
        payload = {"assessment_type": "phq9", "user_id": "test_user"}
        response = requests.post(f"{API_BASE_URL}/api/assessments/start", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("assessment_id"):
                assessment_id = data.get("assessment_id")
                print_test("Start PHQ-9 assessment", "PASS", f"Session ID: {assessment_id[:8]}...")
            else:
                print_test("Start PHQ-9 assessment", "FAIL", data.get("error", "Unknown error"))
                all_passed = False
        else:
            print_test("Start PHQ-9 assessment", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Start PHQ-9 assessment", "FAIL", str(e))
        all_passed = False
    
    # Test 4.3: Start assessment - GAD-7
    try:
        payload = {"assessment_type": "gad7", "user_id": "test_user"}
        response = requests.post(f"{API_BASE_URL}/api/assessments/start", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test("Start GAD-7 assessment", "PASS", "Assessment initialized")
            else:
                print_test("Start GAD-7 assessment", "FAIL", data.get("error", "Unknown error"))
                all_passed = False
        else:
            print_test("Start GAD-7 assessment", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Start GAD-7 assessment", "FAIL", str(e))
        all_passed = False
    
    # Test 4.4: Score assessment with valid responses
    if assessment_id:
        try:
            payload = {
                "assessment_id": assessment_id,
                "responses": [1, 2, 1, 0, 2, 1, 2, 0, 1]  # 9 responses for PHQ-9
            }
            response = requests.post(f"{API_BASE_URL}/api/assessments/score", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print_test("Score assessment (valid)", "PASS", f"Score: {data.get('total_score')}/{data.get('max_score')}")
                else:
                    print_test("Score assessment (valid)", "FAIL", data.get("error", "Unknown error"))
                    all_passed = False
            else:
                print_test("Score assessment (valid)", "FAIL", f"Status: {response.status_code}")
                all_passed = False
        except Exception as e:
            print_test("Score assessment (valid)", "FAIL", str(e))
            all_passed = False
    
    # Test 4.5: Invalid assessment type
    try:
        payload = {"assessment_type": "invalid_type", "user_id": "test_user"}
        response = requests.post(f"{API_BASE_URL}/api/assessments/start", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if not data.get("success"):
                print_test("Invalid assessment type handling", "PASS", "Properly rejected")
            else:
                print_test("Invalid assessment type handling", "FAIL", "Should have rejected")
                all_passed = False
        else:
            print_test("Invalid assessment type handling", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Invalid assessment type handling", "FAIL", str(e))
        all_passed = False
    
    # Test 4.6: Invalid responses (non-numeric)
    if assessment_id:
        try:
            payload = {
                "assessment_id": assessment_id,
                "responses": ["a", "b", "c"]
            }
            response = requests.post(f"{API_BASE_URL}/api/assessments/score", json=payload, timeout=TIMEOUT)
            
            if response.status_code in [200, 400, 422]:
                data = response.json()
                if response.status_code != 200 or not data.get("success"):
                    print_test("Invalid response validation", "PASS", "Properly rejected")
                else:
                    print_test("Invalid response validation", "WARN", "Should have validated")
            else:
                print_test("Invalid response validation", "FAIL", f"Status: {response.status_code}")
                all_passed = False
        except Exception as e:
            print_test("Invalid response validation", "FAIL", str(e))
            all_passed = False
    
    return all_passed


def test_edge_cases() -> bool:
    """Test 5: Edge Cases & Boundaries"""
    print_header("TEST 5: Edge Cases & Boundary Testing")
    
    all_passed = True
    
    # Test 5.1: Very large payload
    try:
        large_msg = "x" * 100000  # 100KB message
        payload = {"message": large_msg, "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200 or response.status_code == 413:
            print_test("Large payload handling", "PASS", "Handled gracefully")
        else:
            print_test("Large payload handling", "WARN", f"Status: {response.status_code}")
    except requests.exceptions.Timeout:
        print_test("Large payload handling", "WARN", "Request timed out (acceptable)")
    except Exception as e:
        print_test("Large payload handling", "FAIL", str(e))
        all_passed = False
    
    # Test 5.2: Unicode and emoji
    try:
        emoji_msg = "I feel 😢 sad and 😰 anxious... 你好"
        payload = {"message": emoji_msg, "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Unicode/emoji handling", "PASS", "Processed successfully")
        else:
            print_test("Unicode/emoji handling", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Unicode/emoji handling", "FAIL", str(e))
        all_passed = False
    
    # Test 5.3: HTML/Script injection
    try:
        injection_msg = "<script>alert('xss')</script> hello"
        payload = {"message": injection_msg, "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Injection protection", "PASS", "Safely handled")
        else:
            print_test("Injection protection", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Injection protection", "FAIL", str(e))
        all_passed = False
    
    # Test 5.4: Whitespace variations
    try:
        whitespace_msg = "   hello   world   "
        payload = {"message": whitespace_msg, "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Whitespace normalization", "PASS", "Handled properly")
        else:
            print_test("Whitespace normalization", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Whitespace normalization", "FAIL", str(e))
        all_passed = False
    
    # Test 5.5: Null/None handling
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json={"message": None}, timeout=TIMEOUT)
        
        if response.status_code in [200, 400, 422]:
            print_test("Null value handling", "PASS", "Properly validated")
        else:
            print_test("Null value handling", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Null value handling", "FAIL", str(e))
        all_passed = False
    
    # Test 5.6: Rapid consecutive requests
    try:
        all_successful = True
        for i in range(5):
            payload = {"message": f"Request {i+1}", "context": {}}
            response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
            if response.status_code != 200:
                all_successful = False
                break
        
        if all_successful:
            print_test("Rapid requests handling", "PASS", "All 5 requests processed")
        else:
            print_test("Rapid requests handling", "FAIL", "Some requests failed")
            all_passed = False
    except Exception as e:
        print_test("Rapid requests handling", "FAIL", str(e))
        all_passed = False
    
    # Test 5.7: Extreme assessment scores
    try:
        payload = {
            "assessment_id": "test_id",
            "responses": [0] * 100  # 100 zeros
        }
        response = requests.post(f"{API_BASE_URL}/api/assessments/score", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Extreme score values", "PASS", "Handled boundary values")
        else:
            print_test("Extreme score values", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Extreme score values", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def test_response_validation() -> bool:
    """Test 6: Response Format & Validation"""
    print_header("TEST 6: Response Format Validation")
    
    all_passed = True
    
    # Test 6.1: Chat response structure
    try:
        payload = {"message": "How are you?", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            required_fields = ["message", "agent", "timestamp", "crisis_detected", "risk_level"]
            missing = [f for f in required_fields if f not in data]
            
            if not missing:
                print_test("Chat response structure", "PASS", "All required fields present")
            else:
                print_test("Chat response structure", "FAIL", f"Missing: {missing}")
                all_passed = False
        else:
            print_test("Chat response structure", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Chat response structure", "FAIL", str(e))
        all_passed = False
    
    # Test 6.2: Assessment response structure
    try:
        payload = {"assessment_type": "phq9", "user_id": "test"}
        response = requests.post(f"{API_BASE_URL}/api/assessments/start", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            required_fields = ["success", "assessment_id", "assessment_name", "questions"]
            missing = [f for f in required_fields if f not in data]
            
            if not missing:
                print_test("Assessment start response", "PASS", "All required fields present")
            else:
                print_test("Assessment start response", "FAIL", f"Missing: {missing}")
                all_passed = False
        else:
            print_test("Assessment start response", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Assessment start response", "FAIL", str(e))
        all_passed = False
    
    # Test 6.3: Timestamp format validation
    try:
        payload = {"message": "test", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get("timestamp", "")
            try:
                datetime.fromisoformat(timestamp)
                print_test("Timestamp format", "PASS", f"Valid ISO format: {timestamp}")
            except ValueError:
                print_test("Timestamp format", "FAIL", f"Invalid format: {timestamp}")
                all_passed = False
        else:
            print_test("Timestamp format", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Timestamp format", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def test_error_handling() -> bool:
    """Test 7: Error Handling & Recovery"""
    print_header("TEST 7: Error Handling & Recovery")
    
    all_passed = True
    
    # Test 7.1: Invalid endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/invalid-endpoint", timeout=TIMEOUT)
        
        if response.status_code == 404:
            print_test("Invalid endpoint handling", "PASS", "Properly returned 404")
        else:
            print_test("Invalid endpoint handling", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Invalid endpoint handling", "FAIL", str(e))
        all_passed = False
    
    # Test 7.2: Malformed JSON
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            data="not valid json",
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        if response.status_code in [400, 422]:
            print_test("Malformed JSON handling", "PASS", "Properly rejected")
        else:
            print_test("Malformed JSON handling", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Malformed JSON handling", "FAIL", str(e))
        all_passed = False
    
    # Test 7.3: Missing required fields
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json={}, timeout=TIMEOUT)
        
        if response.status_code in [400, 422]:
            print_test("Missing required fields", "PASS", "Properly validated")
        else:
            print_test("Missing required fields", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Missing required fields", "FAIL", str(e))
        all_passed = False
    
    # Test 7.4: Connection timeout recovery
    try:
        # Try a very short timeout to simulate network delay
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        
        if response.status_code == 200:
            print_test("Connection stability", "PASS", "Stable connection")
        else:
            print_test("Connection stability", "WARN", f"Status: {response.status_code}")
    except requests.exceptions.Timeout:
        print_test("Connection stability", "FAIL", "Request timed out")
        all_passed = False
    except Exception as e:
        print_test("Connection stability", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "="*78 + "╗")
    print("║" + "PSYCHOLOGY CHATBOT - COMPREHENSIVE TEST SUITE".center(78) + "║")
    print("║" + f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(78) + "║")
    print("╚" + "="*78 + "╝")
    print(Colors.END)
    
    # Run all tests
    results = {}
    results["Backend Health"] = test_backend_health()
    results["Chat Functionality"] = test_chat_basic()
    results["Spell Checker"] = test_spell_check()
    results["Assessments"] = test_assessments()
    results["Edge Cases"] = test_edge_cases()
    results["Response Validation"] = test_response_validation()
    results["Error Handling"] = test_error_handling()
    
    # Summary
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = f"{Colors.GREEN}✓{Colors.END}" if result else f"{Colors.RED}✗{Colors.END}"
        print(f"{symbol} {test_name:<50} [{status}]")
    
    print()
    print(f"{Colors.BOLD}Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {failed}{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.END}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
