# Unified BDD Linter - IDE Plugins & Integrations

This directory contains IDE extensions and integrations for the Unified BDD Linter.

## VS Code Extension

A full-featured VS Code extension that provides real-time Gherkin file validation directly in the editor.

### Features

✅ **Real-time Linting** - Validates as you type and on file save
✅ **Inline Diagnostics** - Shows violations with squiggles and hover information  
✅ **Quick Fixes** - Auto-fix suggestions and bulk auto-fixing
✅ **Folder Linting** - Lint all features in a folder from context menu
✅ **Configuration** - Fully customizable via VS Code settings
✅ **Command Palette** - Easy access to all commands

### Installation

1. Copy the entire plugin directory to VS Code extensions folder:
```bash
mkdir -p ~/.vscode/extensions/unified-bdd-linter
cp -r . ~/.vscode/extensions/unified-bdd-linter
```

2. Or package as VSIX:
```bash
npm install -g vsce
vsce package
code --install-extension unified-bdd-linter-1.0.0.vsix
```

### Usage

**Keyboard Shortcuts:**
- `Ctrl+Shift+L` (Windows/Linux) or `Cmd+Shift+L` (Mac) - Lint current file

**Commands (via Command Palette):**
- `Unified BDD Linter: Lint Gherkin File` - Lint current file
- `Unified BDD Linter: Auto-fix Gherkin File` - Auto-fix current file  
- `Unified BDD Linter: Lint All Features in Folder` - Lint folder from explorer

**Context Menu:**
- Right-click on .feature file → "Lint Gherkin File"
- Right-click on .feature file → "Auto-fix Gherkin File"
- Right-click on folder → "Lint All Features in Folder"

### Configuration

```json
{
  "unified-bdd-linter.enable": true,
  "unified-bdd-linter.autoLintOnSave": true,
  "unified-bdd-linter.minSeverity": "warning",
  "unified-bdd-linter.showSuggestions": true,
  "unified-bdd-linter.linterPath": ""
}
```

### Screenshot Example

When you open a .feature file with violations:
```
Scenario: User Logs In
  ✗ ST001: Unnamed feature (Error)
  ✗ ST002: Unnamed scenario (Error)  
  → Use business language instead of UI actions
  Given user123 is logged in
  When I click the login button    ← Q001: Implementation detail
```

---

## Python Bridge (vscode_bridge.py)

Communication layer between VS Code extension and Python linter.

### Usage

```bash
python vscode_bridge.py /path/to/feature.feature
```

### Output Format

```json
{
  "file": "/path/to/feature.feature",
  "diagnostics": [
    {
      "range": {
        "start": {"line": 0, "character": 0},
        "end": {"line": 0, "character": 10}
      },
      "severity": 0,
      "code": "ST001",
      "source": "Unified BDD Linter",
      "message": "Feature must have a name",
      "data": {
        "rule_name": "Unnamed feature",
        "suggestion": "Add a descriptive feature title",
        "category": "structure"
      }
    }
  ]
}
```

---

## JetBrains IDEs Integration (IntelliJ, WebStorm, etc.)

### Setup

1. Install "Gherkin" plugin from JetBrains marketplace
2. Configure external tool for linting:

**File → Settings → Tools → External Tools → Add:**

| Field | Value |
|-------|-------|
| Name | Unified BDD Linter |
| Program | `python` |
| Arguments | `$ProjectFileDir$/linter.py $FilePath$` |
| Working Directory | `$ProjectFileDir$` |
| Output Filters | *.feature |

### Usage

- Right-click .feature file → "External Tools" → "Unified BDD Linter"
- View output in "Run" tool window

---

## GitHub Actions Integration

### Workflow File

```yaml
name: Lint Gherkin Features

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Lint features
        run: |
          cd UnifiedBDDLinter
          python linter.py ../features/ --severity error
```

---

## Custom IDE Integration

### Generic Bridge Pattern

For any IDE/editor, implement this pattern:

```python
from linter import UnifiedLinter
import json
import sys

file_path = sys.argv[1]
linter = UnifiedLinter()
violations = linter.lint_file(file_path)

# Convert to IDE format
output = {
    "file": file_path,
    "violations": [
        {
            "line": v.line,
            "column": v.column,
            "severity": v.severity.value,
            "message": v.message,
            "rule": v.rule_id
        }
        for v in violations
    ]
}

print(json.dumps(output))
```

---

## Vim/Neovim Integration

### Using ALE Plugin

Add to `.vimrc`:

```vim
let g:ale_linters = {
    \ 'gherkin': ['unified_bdd_linter']
    \ }

let g:ale_linters_ignore = {}

let g:ale_fixers = {
    \ 'gherkin': ['unified_bdd_auto_fix']
    \ }
```

### Using Coc.nvim

```json
{
  "languageserver": {
    "unified-bdd-linter": {
      "command": "python",
      "args": ["/path/to/vscode_bridge.py"],
      "filetypes": ["gherkin"]
    }
  }
}
```

---

## Sublime Text Integration

### Using SublimeLinter

1. Install SublimeLinter package
2. Create custom linter plugin:

```python
from SublimeLinter.lint import Linter
import json
import subprocess

class UnifiedBdd(Linter):
    syntax = 'gherkin'
    cmd = 'python linter.py'
    
    def parse_output(self, output):
        try:
            data = json.loads(output)
            for violation in data.get('violations', []):
                yield {
                    'line': violation['line'] - 1,
                    'col': violation['column'],
                    'error': violation['message']
                }
        except:
            pass
```

---

## Configuration Files

### `.unified-lintrc.json` Locations

The linter searches for configuration in this order:
1. Current working directory
2. Project root
3. Home directory
4. Built-in defaults

---

## Troubleshooting

### Extension Not Detecting Linter

1. Check if `linter.py` is in the workspace root:
```bash
find . -name "linter.py" -type f
```

2. Set explicit path in VS Code settings:
```json
"unified-bdd-linter.linterPath": "/full/path/to/linter.py"
```

### Auto-fix Not Working

1. Ensure `auto_fix.py` is present
2. Check Python permissions:
```bash
chmod +x auto_fix.py
```

3. Test manually:
```bash
python auto_fix.py features/my-feature.feature --dry-run
```

### Linting Slow

1. Exclude large directories in settings:
```json
"unified-bdd-linter.ignoredPaths": [
  "node_modules/**",
  "dist/**"
]
```

2. Reduce auto-lint frequency in settings

---

## Contributing

To add support for a new IDE:

1. Create `<ide>_integration.py` or `<ide>_bridge.py`
2. Implement JSON output format
3. Document setup steps
4. Add to this README

---

## Support

- **Issues**: Report bugs on GitHub
- **Features**: Request enhancements via issues
- **Questions**: See main README.md

---

**Ready to lint Gherkin in your favorite IDE? Choose your platform above!**
