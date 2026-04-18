# PyDriller Mining Setup Complete! 🚀

## What We've Created

### 1. **Core Mining Engine**
- **`pydriller_feature_miner.py`** - Main PyDriller mining class
  - Mines Git repositories for .feature files
  - Extracts Gherkin scenarios from commit history
  - Tracks feature evolution (commits, authors, dates)
  - Generates detailed reports

### 2. **Integration Layer**
- **`mining_integration.py`** - Combines PyDriller + GitHub API
  - Runs integrated mining pipeline
  - Enhances data with stability/complexity metrics
  - Generates unified dataset
  - Creates comprehensive reports

### 3. **Interactive CLI**
- **`pydriller_quickstart.py`** - User-friendly mining interface
  - Option 1: Mine single repository
  - Option 2: Mine multiple popular BDD repos
  - Option 3: Run integrated pipeline
  - Option 4: Mine custom repositories

### 4. **Documentation**
- **`PYDRILLER_MINING_GUIDE.md`** - Complete guide with examples
- **`pydriller_requirements.txt`** - Dependencies

---

## Quick Start

### Step 1: Install PyDriller
```bash
cd /home/vaishnavkoka/RE4BDD/Mining
pip install -r pydriller_requirements.txt
```

### Step 2: Run Interactive Mining
```bash
python pydriller_quickstart.py
```

Or run directly in Python:

### Step 3: Mine a Repository
```python
from pydriller_feature_miner import PyDrillerFeatureMiner

miner = PyDrillerFeatureMiner(output_prefix="my_project")

# Mine single repo
miner.mine_repository(
    repo_url="https://github.com/cucumber/cucumber-js",
    repo_name="Cucumber JS",
    branch="main"
)

miner._export_results()
```

---

## Key Features

### ✅ Deep Git History
- Analyzes ALL commits affecting .feature files
- Tracks author, date, changes per commit
- Identifies feature lifecycle (when added/modified/removed)

### ✅ Scenario Extraction
- Extracts Gherkin scenario names from feature files
- Deduplicates scenarios across commits
- Counts scenarios per file

### ✅ Stability Analysis
- **New**: < 2 commits (recent)
- **Emerging**: 2-4 commits (being refined)
- **Stable**: 5-14 commits (established)
- **Mature**: 15+ commits (core feature)

### ✅ Complexity Classification
- **Low**: 1-2 scenarios
- **Medium**: 3-9 scenarios
- **High**: 10+ scenarios

### ✅ Rich Metadata
- Commit history per feature
- Authors tracking
- First seen / Last modified dates
- Step definition languages detected
- Lines added/deleted per commit

---

## Output Files

After mining, you'll get:

| File | Contents |
|------|----------|
| `pydriller_features.csv` | Feature list with scenario counts |
| `pydriller_repositories.json` | Full repo data with commit history |
| `pydriller_summary.txt` | Human-readable mining report |
| `integrated_bdd_mining_dataset.csv` | Enhanced dataset (if using integration) |
| `integrated_mining_report.txt` | Comprehensive analysis |

---

## Integration with Your RAGAS Evaluation

You can now feed PyDriller-mined scenarios into your RAGAS evaluation pipeline:

```python
# Load mined features
import pandas as pd
features_df = pd.read_csv("mining_outputs/pydriller_features.csv")

# Extract scenarios
all_scenarios = []
for scenarios_str in features_df['scenarios']:
    if pd.notna(scenarios_str):
        scenarios = scenarios_str.split(' | ')
        all_scenarios.extend(scenarios)

# Use in your RAGAS notebook (ragas_eval_requirements.ipynb)
# Feed these as questions with repository context
```

---

## Repository Examples

Popular BDD repositories to mine:

```python
repositories = [
    # JavaScript / Node.js
    {
        "url": "https://github.com/cucumber/cucumber-js",
        "name": "Cucumber JavaScript",
        "branch": "main"
    },
    # Python / Behave
    {
        "url": "https://github.com/behave/behave",
        "name": "Behave (Python BDD)",
        "branch": "master"
    },
    # Java / Cucumber-JVM
    {
        "url": "https://github.com/cucumber/cucumber-jvm",
        "name": "Cucumber JVM",
        "branch": "main"
    },
    # Python / pytest-BDD
    {
        "url": "https://github.com/pytest-dev/pytest-bdd",
        "name": "pytest-BDD",
        "branch": "master"
    },
    # API Testing / Dredd
    {
        "url": "https://github.com/apiaryio/dredd",
        "name": "Dredd (API Testing)",
        "branch": "master"
    },
]
```

---

## Workflow

```
GitHub Repositories
        ↓
    PyDriller
        ↓
Git History Analysis
        ↓
Feature Extraction
        ↓
Scenario Identification
        ↓
Dataset Generation (CSV + JSON)
        ↓
Integration Layer
        ↓
Stability & Complexity Metrics
        ↓
Unified Mining Dataset
        ↓
RAGAS Evaluation Pipeline
        ↓
Metric Results (49.2% Answer Relevancy!)
```

---

## Next Steps

1. ✅ Install PyDriller
2. ✅ Run `pydriller_quickstart.py`
3. ✅ Mine your first repository
4. ✅ Load results into Pandas DataFrame
5. ✅ Use scenarios for RAGAS evaluation
6. ✅ Improve metrics through prompt engineering

---

## Comparison: PyDriller vs GitHub API

Your existing setup uses GitHub API search. PyDriller adds:

| Feature | GitHub API | PyDriller |
|---------|----------|-----------|
| Find features | ✅ Fast | ✅ Thorough |
| Clone repos | ✅ | ✅ Automatic |
| Feature history | ❌ | ✅ Complete |
| Scenarios per feature | ✅ (quick) | ✅ Detailed |
| Author tracking | ❌ | ✅ Full |
| Stability analysis | ❌ | ✅ Detected |
| Step definitions | ✅ (find) | ✅ Analyze |
| Performance | ⚡ Fast | 🔍 Thorough |

**Use both:**
- GitHub API: Quick discovery of features
- PyDriller: Deep analysis and history

---

## Files Location

```
/home/vaishnavkoka/RE4BDD/Mining/
├── pydriller_feature_miner.py      (Core engine)
├── mining_integration.py            (Integration layer)
├── pydriller_quickstart.py          (Interactive CLI)
├── pydriller_requirements.txt       (Dependencies)
├── PYDRILLER_MINING_GUIDE.md        (Full documentation)
└── mining_outputs/
    ├── pydriller_features.csv
    ├── pydriller_repositories.json
    ├── pydriller_summary.txt
    ├── integrated_bdd_mining_dataset.csv
    └── integrated_mining_report.txt
```

---

## Ready to Mine!

Your PyDriller mining setup is complete and ready to use. Start with:

```bash
python pydriller_quickstart.py
```

This will give you a deep, historical analysis of BDD features from GitHub repositories!

Happy mining! 🚀
