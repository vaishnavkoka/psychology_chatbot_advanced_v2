# PyDriller-Based BDD Feature Mining

## Overview

This module uses **PyDriller** to mine BDD (Behavior-Driven Development) features from GitHub repositories at the Git commit level. Unlike simple GitHub API searches, PyDriller provides:

- 🔍 **Deep Git History Analysis**: Tracks how features evolve over commits
- 📊 **Commit-Level Metadata**: Author, date, changes, diff analysis
- 🎯 **Feature Evolution Tracking**: See when scenarios were added/modified/removed
- 🏗️ **Complete Repository Context**: Step definitions, supporting code, architecture
- 🔗 **Author Attribution**: Track who created and modified BDD scenarios

## Components

### 1. `pydriller_feature_miner.py`
**Core PyDriller mining engine**

```python
from pydriller_feature_miner import PyDrillerFeatureMiner

# Mine a single repository
miner = PyDrillerFeatureMiner(output_prefix="my_mining")
repo_data = miner.mine_repository(
    repo_url="https://github.com/cucumber/cucumber-js",
    repo_name="Cucumber JavaScript",
    branch="main"
)

# Mine multiple repositories
repositories = [
    {"url": "...", "name": "...", "branch": "main"},
    {"url": "...", "name": "...", "branch": "main"},
]
miner.mine_multiple_repositories(repositories)
```

**Outputs:**
- `pydriller_features.csv` - Extracted features with scenario counts
- `pydriller_repositories.json` - Detailed repo data with full commit history
- `pydriller_summary.txt` - Human-readable mining report

**Key Metrics Collected:**
- Feature file paths and scenario counts
- Commit history (commits modifying features)
- First seen date and last modified date
- Authors who created/modified features
- Added/deleted lines per commit
- Step definition languages detected

### 2. `mining_integration.py`
**Integration layer combining PyDriller + GitHub API**

```python
from mining_integration import BDDMiningIntegration

integration = BDDMiningIntegration()
results = integration.run_integrated_mining(repositories)
```

**Creates:**
- `integrated_bdd_mining_dataset.csv` - Unified dataset with all metrics
- `integrated_mining_report.txt` - Comprehensive analysis

**Enhancements:**
- Feature stability score (new → emerging → stable → mature)
- Complexity classification (low → medium → high based on scenario count)
- Timestamp tracking
- Aggregated statistics

### 3. `pydriller_quickstart.py`
**Interactive CLI for easy mining**

```bash
python pydriller_quickstart.py
```

Options:
1. Mine a single repository (quick)
2. Mine multiple popular BDD repositories
3. Run integrated mining pipeline
4. Mine custom repositories
0. Exit

## Usage Examples

### Example 1: Mine Cucumber JavaScript

```python
from pydriller_feature_miner import PyDrillerFeatureMiner

miner = PyDrillerFeatureMiner(output_prefix="cucumber_js")
miner.mine_repository(
    repo_url="https://github.com/cucumber/cucumber-js",
    repo_name="Cucumber JavaScript",
    branch="main"
)
miner._export_results()
```

### Example 2: Mine Multiple Repositories

```python
repositories = [
    {
        "url": "https://github.com/cucumber/cucumber-js",
        "name": "Cucumber JS",
        "branch": "main"
    },
    {
        "url": "https://github.com/cucumber/cucumber-python",
        "name": "Cucumber Python",
        "branch": "main"
    },
]

miner = PyDrillerFeatureMiner()
miner.mine_multiple_repositories(repositories)
```

### Example 3: Integrated Mining with Enhancement

```python
from mining_integration import BDDMiningIntegration

integration = BDDMiningIntegration()
results = integration.run_integrated_mining(repositories)

# Access results
integrated_df = results["integrated_dataset"]
summary = results["summary"]

print(f"Found {len(integrated_df)} feature files")
print(f"Total scenarios: {summary['total_scenarios']}")
print(f"Feature stability distribution:")
for stability, count in summary['stability_distribution'].items():
    print(f"  {stability}: {count}")
```

## Output Files

### CSV Outputs

**`pydriller_features.csv`** - Feature-level metrics
```
repo_name | feature_file | scenario_count | scenarios | commits | first_seen | last_modified
```

**`integrated_bdd_mining_dataset.csv`** - Enhanced dataset
```
repo_name | feature_file | scenario_count | commits | feature_stability | complexity_score | extracted_at | mining_method
```

### JSON Outputs

**`pydriller_repositories.json`** - Full repository data
```json
[
  {
    "repo_url": "...",
    "repo_name": "...",
    "feature_files": [
      {
        "file_path": "features/login.feature",
        "scenario_count": 5,
        "scenarios": ["User logs in", "Invalid credentials", ...],
        "commits_count": 12,
        "authors": ["John Doe", "Jane Smith"],
        "commit_history": [...]
      }
    ],
    "total_scenarios": 45,
    "languages_in_steps": ["Python", "JavaScript"]
  }
]
```

## Feature Stability Classification

Features are classified based on commit frequency:

| Stability | Commits | Meaning |
|-----------|---------|---------|
| **new** | < 2 | Recently added, may change |
| **emerging** | 2-4 | Growing, being refined |
| **stable** | 5-14 | Established, rarely modified |
| **mature** | 15+ | Core feature, long history |

## Complexity Classification

Features are scored by scenario count:

| Complexity | Scenarios | Meaning |
|-----------|-----------|---------|
| **low** | 1-2 | Simple feature |
| **medium** | 3-9 | Moderate coverage |
| **high** | 10+ | Complex feature set |

## Key Advantages Over GitHub API

| Aspect | GitHub API | PyDriller |
|--------|-----------|-----------|
| **Git History** | ❌ Limited | ✅ Full |
| **Commit Details** | Basic | Rich metadata |
| **Author Tracking** | ❌ | ✅ Complete |
| **Feature Evolution** | ❌ | ✅ Tracked |
| **Step Definitions** | Find only | Analyze |
| **Feature Stability** | Not tracked | Detected |
| **Performance** | Fast | Thorough |

## Mining Large Repositories

For large repositories, PyDriller can take time. Tips:

1. **Use branch filtering**: Only analyze relevant branches
2. **Limit commits**: PyDriller defaults to all commits
3. **Cache results**: Save extracted data as CSV for reuse
4. **Parallel mining**: Mine different repos in parallel

## Integration with RAGAS Evaluation

After mining, you can use the extracted scenarios for RAGAS evaluation:

```python
# Load mined features
import pandas as pd
features_df = pd.read_csv("mining_outputs/pydriller_features.csv")

# Extract scenarios for evaluation
scenarios = features_df['scenarios'].str.split(' | ').explode().unique()

# Use in RAGAS pipeline
# (See ragas_eval_requirements.ipynb)
```

## Troubleshooting

### Issue: "Repository not found"
- Ensure GitHub URL is correct
- Try HTTPS URL instead of SSH

### Issue: "Clone timeout"
- Increase `clone_timeout_seconds` in mining_config.py
- Try cloning repository manually first to verify access

### Issue: "ModuleNotFoundError: No module named 'pydriller'"
```bash
pip install -r pydriller_requirements.txt
```
Or directly:
```bash
pip install pydriller==2.9
```

### Issue: GitHub API rate limiting (if using GitHub search)
- Use GitHub token: `export GITHUB_TOKEN=your_token`
- Wait for rate limit reset
- See: https://github.com/settings/tokens

## Future Enhancements

- [ ] Parallel repository cloning
- [ ] Incremental mining (only new commits)
- [ ] Semantic analysis of scenario changes
- [ ] Feature complexity scoring based on steps
- [ ] Step definition code analysis
- [ ] Performance metrics per scenario
- [ ] Integration with BDD test results

## References

- [PyDriller Documentation](https://pydriller.readthedocs.io/) (Version 2.9 documented here)
- [PyDriller GitHub](https://github.com/mauricioaniche/pydriller)
- [Gherkin Language Reference](https://cucumber.io/docs/gherkin/)
- [Cucumber/Behave/Pytest-BDD Examples](https://github.com/cucumber)
