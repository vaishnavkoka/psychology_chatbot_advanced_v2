#!/bin/bash
#
# BDD Linter Fix Workflow
# One-command script to lint and auto-fix all feature files
#

echo "🔍 BDD Linter & Auto-fix Workflow"
echo "=================================="
echo ""

# Step 1: Run linter on originals
echo "📊 Step 1: Analyzing original features/"
python3 linter.py features/ | tail -5
echo ""

# Step 2: Auto-fix in place
echo "🔧 Step 2: Auto-fixing and saving to fixed_features/"
python3 auto_fix.py features/ --output fixed_features/
echo ""

# Step 3: Verify
echo "✅ Step 3: Verifying fixed_features/"
python3 linter.py fixed_features/ | tail -5
echo ""

echo "=================================="
echo "✓ Workflow complete!"
