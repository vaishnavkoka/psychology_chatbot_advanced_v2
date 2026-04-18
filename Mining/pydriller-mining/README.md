
# PyDriller BDD Mining Suite

Welcome to the PyDriller-based BDD feature mining module! This folder contains all the tools and scripts needed to mine Gherkin BDD scenarios from GitHub repositories using deep Git history analysis.

## 📁 Folder Structure

```
pydriller-mining/
├── README.md (this file)
├── pydriller_feature_miner.py       # Core mining engine
├── mining_integration.py             # Integration with GitHub API
├── pydriller_quickstart.py          # Interactive CLI tool
├── github_pydriller_dataset_miner.py # Production dataset miner
├── pydriller_requirements.txt       # Python dependencies
├── PYDRILLER_MINING_GUIDE.md        # Comprehensive documentation
└── PYDRILLER_SETUP_COMPLETE.md      # Quick reference guide
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /home/vaishnavkoka/RE4BDD/Mining/pydriller-mining
pip install -r pydriller_requirements.txt
```

### 2. Run Interactive Mining
```bash
python pydriller_quickstart.py
```

### 3. Run Robust Dataset Miner (recommended)

First, set your GitHub token (required for reasonable rate limits):
```bash
export GITHUB_TOKEN=YOUR_NEW_TOKEN
```

Then run the miner:
```bash
python3 github_pydriller_dataset_miner.py --max-repos 40 --min-stars 30 --min-feature-files 2 --workers 6 --since 2021-01-01 --min-steps 3
```

If you hit rate limits or don't want to verify every repository's feature file count:
```bash
# Skip verification to save API calls (faster, but may include some repos without .feature files):
python3 github_pydriller_dataset_miner.py --max-repos 40 --min-stars 30 --skip-verification=true --workers 6 --min-steps 3
```

This command creates a deduplicated scenario-level dataset in `mining_outputs/` with repository-level `train/val/test` splits.
Discovery is language-agnostic and strictly keeps only repositories with confirmed `.feature` files (unless --skip-verification is used).

Useful flags:
- `--max-repos 40`: number of repositories to mine
- `--min-stars 30`: minimum stars for repository discovery
- `--min-feature-files 2`: require at least N confirmed `.feature` files per repository
- `--skip-verification=true`: skip .feature count verification per repo to save API calls (faster but riskier)
- `--workers 6`: parallel repository mining for faster throughput
- `--since 2021-01-01 --until 2025-12-31`: time-bounded mining window
- `--min-steps 3 --max-steps 30`: quality filter by scenario step depth
- `--keep-outlines-only`: keep only `Scenario Outline` rows

Rate limit troubleshooting:
- Without token: 60 API requests/hour → ~5-10 repositories before hitting limit
- With token: 5000 API requests/hour → ~200-300 repositories before hitting limit
- If you still hit limits, use `--skip-verification=true` to skip per-repo verification (saves ~1 API call per repo)

Or use Python directly:

```python
from pydriller_feature_miner import PyDrillerFeatureMiner

miner = PyDrillerFeatureMiner(output_prefix="my_mining")
miner.mine_repository(
    repo_url="https://github.com/cucumber/cucumber-js",
    repo_name="Cucumber JS",
    branch="main"
)
miner._export_results()
```

## 📚 Files Description

### Core Modules

**`pydriller_feature_miner.py`** (Main Engine)
- `PyDrillerFeatureMiner` class for mining Git repositories
- Methods:
  - `mine_repository()` - Mine single repository
  - `mine_multiple_repositories()` - Mine batch of repositories
  - `_extract_scenarios_from_diff()` - Extract Gherkin scenarios
  - `_export_results()` - Generate CSV, JSON, and text reports

**`mining_integration.py`** (Integration Layer)
- `BDDMiningIntegration` class combining PyDriller + GitHub API
- Enhancements:
  - Feature stability scoring
  - Complexity classification
  - Unified dataset generation
  - Comprehensive reporting

**`pydriller_quickstart.py`** (Interactive CLI)
- User-friendly interface with 4 mining options
- Option 1: Mine single repository
- Option 2: Mine multiple popular BDD repos
- Option 3: Run integrated mining pipeline
- Option 4: Mine custom repositories

### Documentation

**`PYDRILLER_MINING_GUIDE.md`**
- Complete user guide with examples
- Feature stability and complexity classifications
- Output file descriptions
- Usage patterns
- Troubleshooting guide

**`PYDRILLER_SETUP_COMPLETE.md`**
- Quick reference guide
- Setup instructions
- Integration with RAGAS pipeline
- Key features overview

**`pydriller_requirements.txt`**
- Python package dependencies:
  - pydriller ==2.9 (latest stable)
  - pandas >=1.5.0
  - requests >=2.28.0
  - gitpython >=3.1.0

## 🎯 Key Features

✅ **Deep Git History Analysis**
- Analyzes all commits affecting .feature files
- Tracks feature lifecycle (created, modified, removed)

✅ **Scenario Extraction**
- Extracts Gherkin scenario names
- Deduplicates scenarios across commits
- Counts scenarios per feature file

✅ **Stability Classification**
- **new**: < 2 commits (recent)
- **emerging**: 2-4 commits (being refined)
- **stable**: 5-14 commits (established)
- **mature**: 15+ commits (core feature)

✅ **Complexity Scoring**
- **low**: 1-2 scenarios
- **medium**: 3-9 scenarios
- **high**: 10+ scenarios

✅ **Rich Metadata**
- Author attribution
- Commit dates and messages
- Lines added/deleted
- Step definition languages
- Feature evolution timeline

## 📊 Output Files

Mining generates these output files in `../mining_outputs/`:

| File | Description |
|------|-------------|
| `pydriller_features.csv` | Feature list with scenario counts |
| `pydriller_repositories.json` | Full repository data with commit history |
| `pydriller_summary.txt` | Human-readable mining report |
| `integrated_bdd_mining_dataset.csv` | Enhanced dataset with metrics |
| `integrated_mining_report.txt` | Comprehensive analysis |

## 🔗 Integration with RAGAS Evaluation

Use mined scenarios with your RAGAS evaluation pipeline:

```python
import pandas as pd
from ragas_eval_requirements import evaluate_scenarios

# Load mined features
features_df = pd.read_csv("../mining_outputs/pydriller_features.csv")

# Extract scenarios for evaluation
scenarios = []
for scenarios_str in features_df['scenarios']:
    if pd.notna(scenarios_str):
        scenarios.extend(scenarios_str.split(' | '))

# Use in RAGAS pipeline
# (See ../Ragas/ragas_eval_requirements.ipynb)
```

## 📚 Popular Repositories to Mine

```python
repositories = [
    {"url": "https://github.com/cucumber/cucumber-js", "name": "Cucumber JavaScript", "branch": "main"},
    {"url": "https://github.com/cucumber/cucumber-python", "name": "Cucumber Python", "branch": "main"},
    {"url": "https://github.com/behave/behave", "name": "Behave (Python BDD)", "branch": "master"},
    {"url": "https://github.com/pytest-dev/pytest-bdd", "name": "pytest-BDD", "branch": "master"},
    {"url": "https://github.com/apiaryio/dredd", "name": "Dredd (API Testing)", "branch": "master"},
]
```

## ❓ Common Tasks

### Mine a Single Repository
```bash
python pydriller_quickstart.py
# Select option 1
```

### Mine Multiple Repositories
```bash
python pydriller_quickstart.py
# Select option 2
```

### Mine Custom Repositories
```bash
python pydriller_quickstart.py
# Select option 4
# Enter URLs interactively
```

### Programmatic Mining
```python
from pydriller_feature_miner import PyDrillerFeatureMiner

miner = PyDrillerFeatureMiner()
miner.mine_multiple_repositories([
    {"url": "...", "name": "...", "branch": "main"}
])
```

## 🔍 Troubleshooting

**Issue: ModuleNotFoundError: No module named 'pydriller'**
```bash
pip install -r pydriller_requirements.txt
```

**Issue: Repository not found**
- Verify GitHub URL is correct
- Try HTTPS instead of SSH
- Test: `git clone <url>`

**Issue: Clone timeout**
- Increase timeout in code if needed
- Try cloning repo manually first

**Issue: Rate limiting (GitHub API)**
- Use GitHub token: `export GITHUB_TOKEN=your_token`
- Wait for rate limit reset

## 📖 Documentation

For comprehensive documentation, see:
- [PYDRILLER_MINING_GUIDE.md](PYDRILLER_MINING_GUIDE.md) - Full user guide
- [PYDRILLER_SETUP_COMPLETE.md](PYDRILLER_SETUP_COMPLETE.md) - Setup and quick reference
- [PyDriller Official Docs](https://pydriller.readthedocs.io/)

## 🎓 Workflow Example

```
1. Run: python pydriller_quickstart.py
   ↓
2. Select mining option
   ↓
3. PyDriller clones & analyzes repository
   ↓
4. Extracts scenarios from Git history
   ↓
5. Generates CSV/JSON/text reports
   ↓
6. Load results in Pandas
   ↓
7. Use scenarios for RAGAS evaluation
   ↓
8. Improve BDD metrics!
```

## 🚀 Next Steps

1. ✅ Install PyDriller: `pip install -r pydriller_requirements.txt`
2. ✅ Run interactive CLI: `python pydriller_quickstart.py`
3. ✅ Mine your first repository
4. ✅ Load results and explore
5. ✅ Use scenarios for RAGAS evaluation
6. ✅ Improve BDD quality metrics

Happy mining! 🎉
