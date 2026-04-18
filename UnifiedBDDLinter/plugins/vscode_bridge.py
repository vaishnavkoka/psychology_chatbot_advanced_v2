#!/usr/bin/env python3
"""
Unified BDD Linter - VS Code Extension Integration
Bridge between VS Code and the linter

Usage: python vscode_bridge.py <file_path>
Output: JSON format violations for VS Code Diagnostics API
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from linter import UnifiedLinter, RuleSeverity


def severity_to_vscode(severity: RuleSeverity) -> str:
    """Convert linter severity to VS Code DiagnosticSeverity"""
    mapping = {
        RuleSeverity.INFO: 3,      # Hint
        RuleSeverity.WARNING: 1,   # Warning
        RuleSeverity.ERROR: 0,     # Error
        RuleSeverity.CRITICAL: 0,  # Error
    }
    return mapping.get(severity, 3)


def vscode_output(violations, file_path: str) -> str:
    """Generate VS Code Diagnostics JSON output"""
    diagnostics = []
    
    for v in violations:
        diagnostic = {
            "range": {
                "start": {"line": v.line - 1, "character": v.column - 1},
                "end": {"line": v.line - 1, "character": v.column}
            },
            "severity": severity_to_vscode(v.severity),
            "code": v.rule_id,
            "source": "Unified BDD Linter",
            "message": v.message,
            "data": {
                "rule_name": v.rule_name,
                "suggestion": v.suggestion,
                "category": v.category
            }
        }
        diagnostics.append(diagnostic)
    
    return json.dumps({
        "file": file_path,
        "diagnostics": diagnostics
    }, indent=2)


def main():
    if len(sys.argv) < 2:
        print("Usage: python vscode_bridge.py <file_path>", file=sys.stderr)
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(json.dumps({
            "error": f"File not found: {file_path}"
        }))
        sys.exit(1)
    
    linter = UnifiedLinter()
    violations = linter.lint_file(file_path)
    
    # Output JSON for VS Code
    print(vscode_output(violations, file_path))


if __name__ == '__main__':
    main()
