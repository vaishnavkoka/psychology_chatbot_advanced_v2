#!/usr/bin/env python3
"""
Unified BDD Linter Test Runner
Tests the linter against good and bad feature files
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from linter import UnifiedLinter, RuleSeverity
from pathlib import Path


def test_linter_on_file(file_path: str):
    """Test linter on a single file"""
    print(f"\n{'='*80}")
    print(f"Testing: {file_path}")
    print('='*80)
    
    linter = UnifiedLinter()
    violations = linter.lint_file(file_path)
    
    if not violations:
        print("✓ NO VIOLATIONS FOUND")
        return True
    else:
        print(f"Found {len(violations)} violation(s)\n")
        
        # Group by severity
        by_severity = {}
        for v in violations:
            if v.severity not in by_severity:
                by_severity[v.severity] = []
            by_severity[v.severity].append(v)
        
        # Print by severity level
        for severity in [RuleSeverity.CRITICAL, RuleSeverity.ERROR, RuleSeverity.WARNING, RuleSeverity.INFO]:
            if severity in by_severity:
                print(f"\n[{severity.name.upper()}]")
                for v in by_severity[severity]:
                    print(f"  {v.rule_id}: {v.rule_name}")
                    print(f"    Line {v.line}: {v.message}")
                    if v.suggestion:
                        print(f"    Suggestion: {v.suggestion}")
        
        return len([v for v in violations if v.severity == RuleSeverity.ERROR]) == 0


def run_all_tests():
    """Run tests on example files"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "UNIFIED BDD LINTER TEST SUITE" + " "*30 + "║")
    print("╚" + "="*78 + "╝")
    print("\nThis unified linter combines:")
    print("  • gherkin-lint (18 formatting/style rules)")
    print("  • cuke_linter (25+ workflow/validation rules)")
    print("  • FeatureMate (quality/semantic rules)")
    print("  → Total: 50+ comprehensive validation rules")
    
    test_files = [
        "examples/good_example.feature",
        "examples/bad_example.feature",
        "examples/workflow_violations.feature",
        "examples/quality_issues.feature",
    ]
    
    results = {}
    for test_file in test_files:
        if os.path.exists(test_file):
            results[test_file] = test_linter_on_file(test_file)
        else:
            print(f"\nWarning: {test_file} not found")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Passed: {passed}/{total} files")
    
    for file, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {file}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Test specific file
        test_linter_on_file(sys.argv[1])
    else:
        run_all_tests()
