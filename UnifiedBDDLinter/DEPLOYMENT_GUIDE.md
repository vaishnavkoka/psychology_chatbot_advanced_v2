# Deployment Guide - Team Setup

Complete guide for deploying the Unified BDD Linter across your team and CI/CD pipelines.

---

## Phase 1: Team Installation

### Step 1.1: Clone/Copy Repository

```bash
# Clone project
git clone <repo-url> unified-bdd-linter
cd unified-bdd-linter/UnifiedBDDLinter

# Or copy distributed version
cp -r /path/to/distributed/UnifiedBDDLinter ./
```

### Step 1.2: Install Python Requirements

**Note:** Zero external dependencies!

```bash
# Verify Python version (3.7+)
python3 --version   # Should output 3.7 or higher

# Optional: Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 1.3: Install VS Code Extension (Optional)

For VS Code users:

```bash
# Option A: Direct installation
mkdir -p ~/.vscode/extensions/unified-bdd-linter-1.0.0
cp plugins/* ~/.vscode/extensions/unified-bdd-linter-1.0.0/

# Option B: Package as VSIX (requires npm)
cd plugins
npm install
npx vsce package
code --install-extension unified-bdd-linter-1.0.0.vsix
cd ..
```

### Step 1.4: Create Team Configuration

```bash
# Copy configuration template
cp .unified-lintrc.json .unified-lintrc.json.team

# Edit for team standards
nano .unified-lintrc.json.team  # on Linux/Mac
# or
notepad .unified-lintrc.json.team  # on Windows
```

Example team configuration:
```json
{
  "rules": {
    "enabled": true,
    "disabled": [],
    "severity_overrides": {
      "ST001": "error",      // Feature name required
      "ST002": "error",      // Scenario name required
      "W003": "error",       // Verification step required
      "Q001": "warning"      // Implementation details warning only
    }
  },
  "limits": {
    "max_feature_name": 80,
    "max_scenario_name": 80,
    "max_step_length": 120,
    "max_steps_per_scenario": 8
  },
  "formatting": {
    "indent_size": 2,
    "insert_final_newline": true,
    "trim_trailing_whitespace": true
  },
  "quality": {
    "enforce_business_language": true
  }
}
```

### Step 1.5: Verification Test

```bash
# Test basic functionality
python3 linter.py examples/good_example.feature

# Test configuration
cp .unified-lintrc.json ./
python3 linter.py examples/ --summary

# Test auto-fix
python3 auto_fix.py examples/bad_example.feature --dry-run

echo "✓ Installation complete!"
```

---

## Phase 2: Local Development Setup

### Step 2.1: Development Documentation

Create `docs/DEVELOPER_SETUP.md`:

```markdown
# Developer Setup Guide

## Prerequisites
- Python 3.7+
- Git
- VS Code (optional)

## Setup Steps

1. Clone the repository
2. Navigate to UnifiedBDDLinter directory
3. Install VS Code extension (if using VS Code)
4. Configure .gherkin-lintrc (copy from template)

## Usage Commands

### Lint a feature file
\`\`\`bash
python3 linter.py features/my-feature.feature
\`\`\`

### Fix violations automatically
\`\`\`bash
python3 auto_fix.py features/my-feature.feature --dry-run
python3 auto_fix.py features/my-feature.feature
\`\`\`

### Lint all features
\`\`\`bash
python3 linter.py features/
\`\`\`

## Troubleshooting
- [See main README](../README.md)
```

### Step 2.2: Team Documentation

Create `docs/TEAM_STANDARDS.md`:

```markdown
# BDD Quality Standards

## Feature File Requirements

### Structure (Mandatory)
- [ ] Feature must have descriptive name
- [ ] Minimum 1 Given-When-Then scenario
- [ ] All scenarios named uniquely
- [ ] Use Given-When-Then order (no exceptions)

### Language (Mandatory)
- [ ] Business language only (no UI implementation details)
- [ ] No "click", "type", "scroll" in step descriptions
- [ ] Use "I", "user", "system" consistently
- [ ] No code syntax or SQL

### Style (Recommended)
- [ ] 2-space indentation
- [ ] No trailing spaces
- [ ] Maximum 100 characters per step
- [ ] Maximum 8 steps per scenario

### Violations
| Severity | Action | Example |
|----------|--------|---------|
| **Error** | Fix before merge | Missing scenario name |
| **Warning** | Review in PR | Implementation detail |
| **Info** | Nice to have | Long step description |

## Running Linter

All developers should run before committing:
\`\`\`bash
python3 linter.py features/ --severity error
\`\`\`

All merge requests must pass without errors.
```

### Step 2.3: Pre-commit Hook

Create `.git/hooks/pre-commit` (or use Husky for Node projects):

```bash
#!/bin/bash
# Lint all modified feature files

FEATURES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.feature$')

if [ -z "$FEATURES" ]; then
  exit 0
fi

echo "🔍 Linting feature files..."

cd UnifiedBDDLinter
python3 linter.py $FEATURES --severity error

if [ $? -ne 0 ]; then
  echo "❌ Linting failed! Fix errors before committing."
  exit 1
fi

echo "✓ Linting passed!"
exit 0
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Phase 3: CI/CD Integration

### Option 3.1: GitHub Actions

Create `.github/workflows/lint-features.yml`:

```yaml
name: Lint Gherkin Features

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'features/**/*.feature'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'features/**/*.feature'

jobs:
  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Run Unified BDD Linter
      run: |
        cd UnifiedBDDLinter
        python3 linter.py ../features/ --severity error --format json > lint-report.json
    
    - name: Publish Lint Report
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: lint-report
        path: UnifiedBDDLinter/lint-report.json
    
    - name: Comment on PR
      if: github.event_name == 'pull_request' && failure()
      uses: actions/github-script@v6
      with:
        script: |
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '❌ Gherkin linting failed. Please fix violations before merge.'
          })
```

### Option 3.2: GitLab CI

Create `.gitlab-ci.yml` section:

```yaml
lint-features:
  stage: test
  image: python:3.10
  script:
    - cd UnifiedBDDLinter
    - python3 linter.py ../features/ --severity error
  artifacts:
    reports:
      junit: lint-results.xml
    when: always
  only:
    - merge_requests
    - main
```

### Option 3.3: Jenkins

Create `Jenkinsfile` section:

```groovy
pipeline {
  stages {
    stage('Lint Features') {
      steps {
        sh '''
          cd UnifiedBDDLinter
          python3 linter.py ../features/ --severity error --format json > lint-report.json
        '''
      }
    }
    
    stage('Publish Report') {
      steps {
        archiveArtifacts artifacts: 'UnifiedBDDLinter/lint-report.json'
      }
    }
  }
  
  post {
    failure {
      echo '❌ Feature linting failed!'
    }
  }
}
```

### Option 3.4: Azure DevOps

Create `azure-pipelines.yml` section:

```yaml
- job: LintFeatures
  displayName: 'Lint Gherkin Features'
  pool:
    vmImage: 'ubuntu-latest'
  
  steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.10'
  
  - script: |
      cd UnifiedBDDLinter
      python3 linter.py ../features/ --severity error --format json > $(Build.ArtifactStagingDirectory)/lint-report.json
    displayName: 'Run Unified BDD Linter'
  
  - task: PublishBuildArtifacts@1
    inputs:
      pathToPublish: '$(Build.ArtifactStagingDirectory)'
      artifactName: 'lint-report'
```

---

## Phase 4: Configuration Management

### Step 4.1: Configuration Hierarchy

Linter searches for configuration in this order:

```
1. --config CLI argument
2. .unified-lintrc.json (current directory)
3. .unified-lintrc.json (project root)
4. ~/.unified-lintrc.json (home directory)
5. Built-in defaults
```

### Step 4.2: Multi-Environment Setup

```
project/
├── .unified-lintrc.json              # Loose defaults
├── .unified-lintrc.strict.json       # Pre-merge requirements
├── .unified-lintrc.development.json  # Developer-friendly
│
└── UnifiedBDDLinter/
    └── linter.py
```

**Usage:**

```bash
# Development (more lenient)
python3 linter.py features/ --config .unified-lintrc.development.json

# Pre-merge (strict)
python3 linter.py features/ --config .unified-lintrc.strict.json
```

### Step 4.3: CI/CD with Strict Config

In CI pipeline:

```bash
# Strict validation in CI
python3 linter.py features/ --config .unified-lintrc.strict.json --severity error
```

---

## Phase 5: Team Training

### Training Outline (30 minutes)

**1. Introduction (5 min)**
- What is the Unified BDD Linter?
- Why we use it (quality, consistency)
- What problems it solves

**2. Demo (10 min)**
```bash
# Show basic usage
python3 linter.py features/example.feature

# Show auto-fix
python3 auto_fix.py features/example.feature --dry-run

# Show VS Code integration (if applicable)
```

**3. Common Violations (10 min)**
Rule categories:
- Style rules (fixable)
- Structure rules (manual)
- Workflow rules (critical)
- Quality rules (best practices)

**4. Q&A (5 min)**

### Reference Card

Create `docs/QUICK_REFERENCE.md`:

```markdown
# Quick Reference Card

## Installation
\`\`\`bash
cd project/UnifiedBDDLinter
python3 linter.py features/
\`\`\`

## Common Commands

| Task | Command |
|------|---------|
| Lint one file | \`python3 linter.py features/my.feature\` |
| Lint all | \`python3 linter.py features/\` |
| Show errors only | \`python3 linter.py features/ --severity error\` |
| Auto-fix preview | \`python3 auto_fix.py features/ --dry-run\` |
| Apply fixes | \`python3 auto_fix.py features/\` |
| Show summary | \`python3 linter.py features/ --summary\` |
| Export JSON | \`python3 linter.py features/ --format json\` |

## Common Violations

**S001** - Trailing spaces
→ Run: \`python3 auto_fix.py features/\`

**ST001** - Feature without name
→ Action: Add "Feature: " with description

**W003** - No Then step
→ Action: Add verification step

**Q001** - Implementation detail
→ Action: Use business language
\`\`\`

### Video Tutorial (Optional)

Create tutorial showing:
1. Installation on Windows/Mac/Linux
2. First feature file linting
3. Auto-fixing violations
4. VS Code extension usage
5. Integration with CI/CD

---

## Phase 6: Monitoring & Feedback

### Step 6.1: Collect Metrics

Track in CI/CD:

```bash
# Weekly lint report
REPORT_DATE=$(date +%Y-%m-%d)
python3 linter.py features/ --format json > reports/lint-$REPORT_DATE.json

# Extract metrics
python3 << 'EOF'
import json
from pathlib import Path
from datetime import datetime

reports = sorted(Path('reports').glob('lint-*.json'))
latest = reports[-1]

with open(latest) as f:
    data = json.load(f)
    violations = data.get('violations', [])
    
print(f"Date: {latest.name}")
print(f"Total violations: {len(violations)}")
print(f"By severity: {Counter(v['severity'] for v in violations)}")
print(f"By rule: {Counter(v['rule_id'] for v in violations)}")
EOF
```

### Step 6.2: Monthly Review

```bash
# Generate trend report
python3 scripts/generate_trend_report.py reports/

# Chart violations over time
# Share with team
```

### Step 6.3: Feedback Loop

Every 2 weeks:
1. Review top 3 most common violations
2. Decide: Auto-fix, training, or rule adjustment
3. Update team standards if needed

---

## Phase 7: Troubleshooting Deployment

### Issue: "Python command not found"

**Solution:**
```bash
# Explicit path
/usr/bin/python3 linter.py features/

# Or in CI, use shebang
#! /usr/bin/env python3
```

### Issue: "Features directory not found in CI"

**Solution:**
```bash
# Adjust path relative to script location
cd $(dirname $0)  # Go to script directory
python3 linter.py ../features/
```

### Issue: "Config file not loading"

**Solution:**
```bash
# Verify config exists
ls -la .unified-lintrc.json

# Test JSON validity
python3 -m json.tool .unified-lintrc.json

# Use explicit path
python3 linter.py features/ --config /full/path/.unified-lintrc.json
```

### Issue: "VS Code extension not working"

**Solution:**
```bash
# Check installation path
ls ~/.vscode/extensions/unified-bdd-linter*/

# Restart VS Code
# or run: code --uninstall-extension unified-bdd-linter
#         code --install-extension unified-bdd-linter-1.0.0.vsix
```

---

## Rollout Timeline

### Week 1: Pilot
- Install on 2-3 developers' machines
- Collect feedback
- Update documentation

### Week 2: Team Rollout
- Install for all developers
- Run training session
- Monitor usage

### Week 3: CI/CD Integration
- Add to GitHub Actions/GitLab CI/Jenkins
- Enforce in pull requests
- Share metric reports

### Week 4: Optimization
- Fine-tune configuration
- Automate metric collection
- Establish team standards

---

## Success Metrics

Track these after 1 month:

| Metric | Target | Goal |
|--------|--------|------|
| **Configuration adherence** | >90% | Consistent style |
| **CI pass rate** | >95% | Linting not blocking merge |
| **Auto-fix usage** | >50% | Developers using tool |
| **Violations/file** | <5 | Quality improving |
| **Team satisfaction** | >4/5 | Tool accepted |

---

## Next Steps

1. ✅ Week 1: Follow Phase 1-2 setup
2. ✅ Week 2: Run Phase 3 CI/CD integration
3. ✅ Week 3: Execute Phase 5 training
4. ✅ Week 4: Begin Phase 6 monitoring

---

## Support Resources

- **Setup help**: See README.md in UnifiedBDDLinter/
- **Troubleshooting**: TESTING_ENHANCEMENTS.md
- **Rule details**: INDEX.md
- **IDE setup**: plugins/README.md

---

**Ready to deploy? Start with Phase 1!** ✅
