#!/usr/bin/env python3
"""
Quick Start for Real GitHub Mining
This script provides templates for transitioning from pilot to full mining
"""

# ============================================================================
# STEP 1: Install Dependencies
# ============================================================================
"""
Run once to set up environment:

$ cd /home/vaishnavkoka/RE4BDD/Mining
$ pip install -r mining_requirements.txt

Optional but recommended:
$ pip install jupyter notebook  # For interactive analysis
"""

# ============================================================================
# STEP 2: Set GitHub Token (Optional but Recommended)
# ============================================================================
"""
For real GitHub mining, set token for higher API rate limits:

Unix/Linux/Mac:
$ export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Windows (PowerShell):
> $env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

Get token from: https://github.com/settings/tokens
- Select: public_repo scope only (safe)
- Rate limit: 5000 requests/hour (vs 60 without token)
"""

# ============================================================================
# STEP 3: Run Full GitHub Mining
# ============================================================================
"""
Create a new script (e.g., run_full_mining.py):
"""

from Mining.mining.oss_bdd_mining import BDDMiningPipeline

def run_full_mining():
    """Execute full mining with real GitHub data"""
    print("\n" + "="*70)
    print("FULL GITHUB MINING - Real Data Collection")
    print("="*70)
    
    # Initialize pipeline with REAL GitHub data (not mock)
    pipeline = BDDMiningPipeline(use_mock_data=False)
    
    # Run complete pipeline
    pipeline.run_mining_pipeline()
    
    print("\n✓ Mining complete!")
    print(f"✓ Dataset: {pipeline.config['output']['output_dir']}/bdd_oss_mining_dataset.csv")
    print(f"✓ Valid projects found: {pipeline.valid_projects}")

# To execute:
# if __name__ == "__main__":
#     run_full_mining()


# ============================================================================
# STEP 4: Customize Mining Parameters
# ============================================================================
"""
Edit mining_config.py BEFORE running:

1. Adjust search limits:
   "max_projects_to_scan": 50,  # Start with 50
   
2. Increase to full scale:
   "max_projects_to_scan": 200,  # Comprehensive
   or
   "max_projects_to_scan": 500,  # Very comprehensive

3. Add more search queries:
   GITHUB_SEARCH_QUERIES = [
       'filename:*.feature stars:>50 language:gherkin',
       'path:features/*.feature stars:>50',
       'repo:cucumber/cucumber-ruby .feature',  # Add specific repos
   ]

4. Adjust timeout for slower connections:
   "clone_timeout_seconds": 600,  # 10 minutes instead of 5
"""

# ============================================================================
# STEP 5: Monitor Mining Progress
# ============================================================================
"""
While mining runs:
- Watch the console output for project names
- Look for ✓ (success) or ✗ (failed) indicators
- Monitor time and file size growth
- Check logs for any API errors

If it stops:
- Check internet connection
- Verify GitHub token:
  $ echo $GITHUB_TOKEN
- Check disk space
- Try running again (uses cloning with shallow depth)
"""

# ============================================================================
# STEP 6: Analyze Results
# ============================================================================
"""
After mining completes:

1. Quick analysis:
   $ python3 analyze_dataset.py

2. Load in Python:
"""

import pandas as pd

def analyze_full_results():
    """Analyze the generated dataset"""
    
    df = pd.read_csv('mining_outputs/bdd_oss_mining_dataset.csv')
    
    print("\n=== DATASET OVERVIEW ===")
    print(f"Total rows: {len(df)}")
    print(f"Unique projects: {df['project_id'].nunique()}")
    print(f"Unique features: {df['feature_file_name'].nunique()}")
    
    print("\n=== PROJECTS ===")
    print(df.groupby('project_name').agg({
        'project_url': 'first',
        'github_stars': 'first',
        'feature_file_count': 'first',
        'feature_file_name': 'count',
    }).rename(columns={'feature_file_name': 'rows'}))
    
    print("\n=== STEP DEFINITION LANGUAGES ===")
    print(df['step_definitions_language'].value_counts())
    
    print("\n=== FEATURES PER PROJECT ===")
    print(df.groupby('project_name')['feature_file_name'].nunique().describe())

# ============================================================================
# STEP 7: Filter & Export
# ============================================================================
"""
Filter results for specific analysis:

1. Only projects with step definitions:
   $ df_with_steps = df[df['step_definitions_found'] == True]

2. Only specific language:
   $ df_python = df[df['step_definitions_language'] == 'python']

3. High-quality projects (>100 stars):
   $ df_quality = df[df['github_stars'] > 100]

4. Export filtered data:
   $ df_python.to_csv('python_bdd_projects.csv', index=False)
"""

# ============================================================================
# STEP 8: Validation Checklist
# ============================================================================
"""
Before publishing results, verify:

□ All projects have ≥4 feature files
□ Requirements are properly mapped
□ Step definitions are correctly identified
□ Languages are properly categorized
□ URLs are valid and accessible
□ Timestamps are consistent
□ No duplicate rows
□ File size reasonable (~1-10 MB for 100+ projects)
□ No sensitive data in output
□ CSV is properly formatted
□ Metadata saved with statistics

Run verification:
"""

def verify_dataset_quality():
    """Verify dataset meets quality standards"""
    
    df = pd.read_csv('mining_outputs/bdd_oss_mining_dataset.csv')
    
    issues = []
    
    # Check 1: Minimum features per project
    min_features = df.groupby('project_id')['feature_file_name'].nunique().min()
    if min_features < 4:
        issues.append(f"⚠ Some projects have <4 features (min: {min_features})")
    else:
        print("✓ All projects have ≥4 features")
    
    # Check 2: No duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"⚠ Found {duplicates} duplicate rows")
    else:
        print("✓ No duplicate rows")
    
    # Check 3: Valid URLs
    invalid_urls = df[~df['project_url'].str.startswith('http')].shape[0]
    if invalid_urls > 0:
        issues.append(f"⚠ Found {invalid_urls} invalid URLs")
    else:
        print("✓ All URLs valid")
    
    # Check 4: No missing required fields
    required = ['project_id', 'feature_file_name', 'requirement_text']
    for col in required:
        missing = df[col].isna().sum()
        if missing > 0:
            issues.append(f"⚠ {missing} missing values in '{col}'")
    
    if not issues:
        print("✓ All quality checks passed!")
    
    return issues

# ============================================================================
# STEP 9: Common Issues & Solutions
# ============================================================================
"""
Issue: GitHub API rate limit exceeded
Solution: 
  1. Wait 1 hour for rate limit reset
  2. Set GitHub token for 5000 req/hr
  3. Reduce max_projects_to_scan

Issue: Clone timeout
Solution:
  1. Increase clone_timeout_seconds to 600
  2. Improve internet connection
  3. Try fewer/smaller projects

Issue: No projects found
Solution:
  1. Check GitHub API is accessible
  2. Verify search queries
  3. Try reducing min_stars threshold
  4. Check GITHUB_TOKEN if set

Issue: Permission denied on output
Solution:
  1. Check directory permissions
  2. Try different output directory
  3. Run from a writable location

See MINING_README.md for detailed troubleshooting
"""

# ============================================================================
# STEP 10: Next Analysis Steps
# ============================================================================
"""
After validation, proceed with research:

1. Statistical Analysis:
   - Distribution of feature files per project
   - Language popularity in BDD
   - Requirement coverage patterns

2. Qualitative Analysis:
   - Common feature naming patterns
   - Step definition complexity
   - Requirement specification quality

3. Comparative Analysis:
   - Language-specific patterns (Python vs JavaScript)
   - Correlation with GitHub stars
   - Evolution over time (if mining multiple times)

4. Visualizations:
   - Feature count distribution
   - Language breakdown pie chart
   - Requirement coverage scatter plot
   - Time trends

5. Publication:
   - Write research paper
   - Create visualizations
   - Submit findings
"""

# ============================================================================
# EXECUTION TEMPLATE
# ============================================================================
"""
Complete workflow script:

#!/bin/bash
cd /home/vaishnavkoka/RE4BDD/Mining

# Setup
echo "Installing dependencies..."
pip install -r mining_requirements.txt

# Run mining
echo "Starting GitHub mining..."
python3 << 'EOF'
from oss_bdd_mining import BDDMiningPipeline
pipeline = BDDMiningPipeline(use_mock_data=False)
pipeline.run_mining_pipeline()
EOF

# Analyze
echo "Analyzing results..."
python3 analyze_dataset.py

# Verify
echo "Verifying quality..."
python3 verify_dataset_quality.py

echo "✓ Mining and analysis complete!"
"""

# ============================================================================
# HELPFUL COMMANDS
# ============================================================================
"""
View dataset:
  $ head -5 mining_outputs/bdd_oss_mining_dataset.csv
  $ wc -l mining_outputs/bdd_oss_mining_dataset.csv

View metadata:
  $ cat mining_outputs/mining_metadata.json

Open in Excel:
  $ libreoffice mining_outputs/bdd_oss_mining_dataset.csv

Quick stats:
  $ python3 analyze_dataset.py

Monitor while running:
  $ tail -f *.log  (if logging to file)

Clean up:
  $ rm -rf mining_outputs/old_*
  $ rm -rf /tmp/bdd_mining_*
"""

if __name__ == "__main__":
    print("""
    ================================================================
    BDD OSS MINING - QUICK START GUIDE
    ================================================================
    
    This script contains instructions and code for full mining.
    
    NEXT STEPS:
    1. Install: pip install -r mining_requirements.txt
    2. Configure: Edit mining_config.py
    3. Set token: export GITHUB_TOKEN=your_token
    4. Run: python3 run_full_mining.py
    5. Analyze: python3 analyze_dataset.py
    
    See MINING_README.md for complete documentation
    ================================================================
    """)
