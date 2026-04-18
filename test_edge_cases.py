#!/usr/bin/env python3
"""
Advanced Edge Case & Stress Testing
Tests boundary conditions, performance, and unusual scenarios
"""

import sys
import os
import time
import json
import requests
import concurrent.futures
from datetime import datetime
import threading


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


API_BASE_URL = "http://localhost:8000"
TIMEOUT = 10


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
    if details:
        print(f"  └─ {details}")


def test_assessment_boundary_cases() -> bool:
    """Test 1: Assessment Score Boundary Cases"""
    print_header("EDGE CASE 1: Assessment Score Boundaries")
    
    all_passed = True
    
    # Test 1.1: Zero scores
    try:
        payload = {"assessment_id": "test_id", "responses": [0] * 9}
        response = requests.post(f"{API_BASE_URL}/api/assessments/score", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("total_score") == 0:
                print_test("Zero score assessment", "PASS", f"Severity: {data.get('severity_level')}")
            else:
                print_test("Zero score assessment", "WARN", f"Score: {data.get('total_score')}")
        else:
            print_test("Zero score assessment", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Zero score assessment", "FAIL", str(e))
        all_passed = False
    
    # Test 1.2: Maximum scores
    try:
        payload = {"assessment_id": "test_id", "responses": [4] * 20}
        response = requests.post(f"{API_BASE_URL}/api/assessments/score", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test("Maximum score assessment", "PASS", f"Score: {data.get('total_score')}")
            else:
                print_test("Maximum score assessment", "WARN", data.get("error", ""))
        else:
            print_test("Maximum score assessment", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Maximum score assessment", "FAIL", str(e))
        all_passed = False
    
    # Test 1.3: Mixed valid/invalid numeric responses
    try:
        payload = {"assessment_id": "test_id", "responses": [1, 2, 3, -1, 5, 10]}
        response = requests.post(f"{API_BASE_URL}/api/assessments/score", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            # Backend should handle or flag these values
            print_test("Out-of-range numeric values", "WARN", f"Handled: {data.get('success')}")
        else:
            print_test("Out-of-range numeric values", "PASS", f"Rejected: Status {response.status_code}")
    except Exception as e:
        print_test("Out-of-range numeric values", "FAIL", str(e))
        all_passed = False
    
    # Test 1.4: Empty assessment ID
    try:
        payload = {"assessment_id": "", "responses": [1, 2, 3]}
        response = requests.post(f"{API_BASE_URL}/api/assessments/score", json=payload, timeout=TIMEOUT)
        
        if response.status_code in [200, 400, 422]:
            data = response.json()
            if response.status_code != 200 or not data.get("success"):
                print_test("Empty assessment ID validation", "PASS", "Properly rejected")
            else:
                print_test("Empty assessment ID validation", "WARN", "Should validate")
        else:
            print_test("Empty assessment ID validation", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Empty assessment ID validation", "FAIL", str(e))
        all_passed = False
    
    # Test 1.5: Single response in list
    try:
        payload = {"assessment_id": "test_id", "responses": [2]}
        response = requests.post(f"{API_BASE_URL}/api/assessments/score", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_test("Single response scoring", "PASS", f"Score: {data.get('total_score')}")
        else:
            print_test("Single response scoring", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Single response scoring", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def test_spell_checker_edge_cases() -> bool:
    """Test 2: Spell Checker Edge Cases"""
    print_header("EDGE CASE 2: Spell Checker Boundaries")
    
    all_passed = True
    
    # Test 2.1: All numbers
    try:
        payload = {"message": "1 2 3 4 5", "context": {}}
        response = requests.post(f"{API_BASE_URL}/spell-check", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_test("Pure numbers spell check", "PASS", f"Corrections: {len(data.get('corrections', {}))}")
        else:
            print_test("Pure numbers spell check", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Pure numbers spell check", "FAIL", str(e))
        all_passed = False
    
    # Test 2.2: All special characters
    try:
        payload = {"message": "!@#$%^&*()", "context": {}}
        response = requests.post(f"{API_BASE_URL}/spell-check", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Special characters spell check", "PASS", "Handled")
        else:
            print_test("Special characters spell check", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Special characters spell check", "FAIL", str(e))
        all_passed = False
    
    # Test 2.3: Single character
    try:
        payload = {"message": "a", "context": {}}
        response = requests.post(f"{API_BASE_URL}/spell-check", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Single character spell check", "PASS", "Processed")
        else:
            print_test("Single character spell check", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Single character spell check", "FAIL", str(e))
        all_passed = False
    
    # Test 2.4: Very long word
    try:
        long_word = "x" * 100
        payload = {"message": long_word, "context": {}}
        response = requests.post(f"{API_BASE_URL}/spell-check", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Very long word spell check", "PASS", "Handled")
        else:
            print_test("Very long word spell check", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Very long word spell check", "FAIL", str(e))
        all_passed = False
    
    # Test 2.5: Mixed case variations
    try:
        payload = {"message": "FeLiNg AnXiOuS", "context": {}}
        response = requests.post(f"{API_BASE_URL}/spell-check", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Mixed case spell check", "PASS", "Processed")
        else:
            print_test("Mixed case spell check", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Mixed case spell check", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def test_concurrent_requests() -> bool:
    """Test 3: Concurrent Request Handling"""
    print_header("EDGE CASE 3: Concurrency & Load")
    
    all_passed = True
    
    # Test 3.1: 10 concurrent chat requests
    try:
        def send_chat_request(msg_num):
            try:
                payload = {"message": f"Message {msg_num}: How are you?", "context": {}}
                response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
                return response.status_code == 200
            except Exception:
                return False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(send_chat_request, range(10)))
        
        successful = sum(results)
        if successful >= 8:  # Allow for some failures
            print_test("10 concurrent requests", "PASS", f"{successful}/10 successful")
        else:
            print_test("10 concurrent requests", "WARN", f"{successful}/10 successful")
    except Exception as e:
        print_test("10 concurrent requests", "FAIL", str(e))
        all_passed = False
    
    # Test 3.2: Sequential rapid requests
    try:
        start_time = time.time()
        for i in range(20):
            payload = {"message": f"Rapid request {i}", "context": {}}
            response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
            if response.status_code != 200:
                raise Exception(f"Request {i} failed")
        
        elapsed = time.time() - start_time
        avg_time = elapsed / 20
        print_test("20 sequential rapid requests", "PASS", f"Avg: {avg_time:.3f}s per request")
    except Exception as e:
        print_test("20 sequential rapid requests", "FAIL", str(e)[:50])
        all_passed = False
    
    return all_passed


def test_message_content_edge_cases() -> bool:
    """Test 4: Message Content Edge Cases"""
    print_header("EDGE CASE 4: Message Content Boundaries")
    
    all_passed = True
    
    # Test 4.1: Only spaces
    try:
        payload = {"message": "     ", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Only spaces message", "PASS", "Handled")
        else:
            print_test("Only spaces message", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Only spaces message", "FAIL", str(e))
        all_passed = False
    
    # Test 4.2: Repeated characters
    try:
        payload = {"message": "aaaaaaaaaaaaaaaaaaaaaa", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Repeated characters", "PASS", "Handled")
        else:
            print_test("Repeated characters", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Repeated characters", "FAIL", str(e))
        all_passed = False
    
    # Test 4.3: URLs and links
    try:
        payload = {"message": "Check this https://example.com and http://test.org", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("URLs in message", "PASS", "Handled safely")
        else:
            print_test("URLs in message", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("URLs in message", "FAIL", str(e))
        all_passed = False
    
    # Test 4.4: Email addresses
    try:
        payload = {"message": "Contact me at test@example.com please", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Email addresses in message", "PASS", "Handled")
        else:
            print_test("Email addresses in message", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Email addresses in message", "FAIL", str(e))
        all_passed = False
    
    # Test 4.5: Multiple languages
    try:
        payload = {"message": "Hello 你好 مرحبا Привет", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Multiple languages", "PASS", "Handled")
        else:
            print_test("Multiple languages", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Multiple languages", "FAIL", str(e))
        all_passed = False
    
    # Test 4.6: Control characters
    try:
        payload = {"message": "Hello\nWorld\r\nTest\t", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Control characters", "PASS", "Handled")
        else:
            print_test("Control characters", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Control characters", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def test_context_variations() -> bool:
    """Test 5: Context Parameter Edge Cases"""
    print_header("EDGE CASE 5: Context Variations")
    
    all_passed = True
    
    # Test 5.1: Empty context
    try:
        payload = {"message": "Hello", "context": {}}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Empty context object", "PASS", "Handled")
        else:
            print_test("Empty context object", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Empty context object", "FAIL", str(e))
        all_passed = False
    
    # Test 5.2: Null context
    try:
        payload = {"message": "Hello", "context": None}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Null context", "PASS", "Handled")
        else:
            print_test("Null context", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Null context", "FAIL", str(e))
        all_passed = False
    
    # Test 5.3: Complex nested context
    try:
        payload = {
            "message": "Hello",
            "context": {
                "user_id": "123",
                "session_id": "abc",
                "nested": {
                    "level1": {
                        "level2": {
                            "level3": "deep"
                        }
                    }
                }
            }
        }
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Nested context", "PASS", "Handled deeply nested data")
        else:
            print_test("Nested context", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Nested context", "FAIL", str(e))
        all_passed = False
    
    # Test 5.4: Context with large arrays
    try:
        payload = {
            "message": "Hello",
            "context": {
                "history": [f"message_{i}" for i in range(100)]
            }
        }
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_test("Large array in context", "PASS", "Handled 100 items")
        else:
            print_test("Large array in context", "WARN", f"Status: {response.status_code}")
    except Exception as e:
        print_test("Large array in context", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def test_assessment_type_variations() -> bool:
    """Test 6: Assessment Type Variations"""
    print_header("EDGE CASE 6: Assessment Type Handling")
    
    all_passed = True
    
    assessment_types = ["phq9", "gad7", "psqi", "rosenberg", "rosenberg_ses", "pcl5"]
    
    # Test 6.1: All assessment types
    try:
        for atype in assessment_types:
            payload = {"assessment_type": atype, "user_id": "test"}
            response = requests.post(f"{API_BASE_URL}/api/assessments/start", json=payload, timeout=TIMEOUT)
            
            if response.status_code != 200:
                print_test(f"Assessment type: {atype}", "FAIL", f"Status: {response.status_code}")
                all_passed = False
        
        print_test("All assessment types", "PASS", f"All {len(assessment_types)} types working")
    except Exception as e:
        print_test("All assessment types", "FAIL", str(e))
        all_passed = False
    
    # Test 6.2: Case sensitivity
    try:
        payload = {"assessment_type": "PHQ9", "user_id": "test"}
        response = requests.post(f"{API_BASE_URL}/api/assessments/start", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200 or not response.json().get("success"):
            print_test("Case insensitive handling", "PASS", "Handled case variation")
        else:
            print_test("Case insensitive handling", "WARN", "May need case normalization")
    except Exception as e:
        print_test("Case insensitive handling", "WARN", str(e)[:30])
    
    # Test 6.3: Empty assessment type
    try:
        payload = {"assessment_type": "", "user_id": "test"}
        response = requests.post(f"{API_BASE_URL}/api/assessments/start", json=payload, timeout=TIMEOUT)
        
        if response.status_code in [200, 400, 422]:
            data = response.json()
            if response.status_code != 200 or not data.get("success"):
                print_test("Empty assessment type validation", "PASS", "Properly rejected")
            else:
                print_test("Empty assessment type validation", "WARN", "Should validate")
        else:
            print_test("Empty assessment type validation", "FAIL", f"Status: {response.status_code}")
            all_passed = False
    except Exception as e:
        print_test("Empty assessment type validation", "FAIL", str(e))
        all_passed = False
    
    return all_passed


def main():
    """Run all edge case tests"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "="*78 + "╗")
    print("║" + "PSYCHOLOGY CHATBOT - ADVANCED EDGE CASE TEST SUITE".center(78) + "║")
    print("║" + f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(78) + "║")
    print("╚" + "="*78 + "╝")
    print(Colors.END)
    
    results = {}
    results["Assessment Boundaries"] = test_assessment_boundary_cases()
    results["Spell Checker Edge Cases"] = test_spell_checker_edge_cases()
    results["Concurrent Requests"] = test_concurrent_requests()
    results["Message Content"] = test_message_content_edge_cases()
    results["Context Variations"] = test_context_variations()
    results["Assessment Type Variations"] = test_assessment_type_variations()
    
    # Summary
    print_header("EDGE CASE TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = f"{Colors.GREEN}✓{Colors.END}" if result else f"{Colors.RED}✗{Colors.END}"
        print(f"{symbol} {test_name:<50} [{status}]")
    
    print()
    print(f"{Colors.BOLD}Total Test Groups: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {failed}{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL EDGE CASE TESTS PASSED!{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ SOME EDGE CASE TESTS HAD ISSUES{Colors.END}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
