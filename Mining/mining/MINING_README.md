# OSS BDD Mining Pipeline

A comprehensive tool for mining open source software (OSS) projects to extract BDD (Behavior-Driven Development) artifacts and create a structured dataset.

## Overview

This mining pipeline automatically discovers OSS projects with BDD feature files, extracts test artifacts, maps requirements, and generates a CSV dataset for analysis. The tool is designed for Requirements Engineering research on BDD practices.

### What Gets Extracted

For each qualifying OSS project, the pipeline extracts:

1. **Feature Files** (Gherkin format)
   - Feature file names and content
   - Direct links to files on GitHub
   - Feature-to-project mappings

2. **Requirements** 
   - Extracted from README, requirements files, and documentation
   - Mapped to corresponding feature files
   - Text preview and source file tracking

3. **Step Definitions**
   - Identification of step implementation files
   - Language detection (Python, JavaScript, Java, Ruby)
   - File paths and links

4. **Project Metadata**
   - GitHub stars (quality indicator)
   - Primary language
   - Repository URL
   - Feature file count

## Directory Structure

```
Mining/
├── mining_config.py              # Configuration and constants
├── oss_bdd_mining.py             # Main mining pipeline
├── run_pilot.py                  # Pilot/demo with mock data
├── mining_requirements.txt       # Python dependencies
├── mining_outputs/               # Output directory (auto-created)
│   ├── bdd_oss_mining_dataset.csv
│   └── mining_metadata.json
└── README.md                     # This file
```

## Quick Start - Pilot Run

### 1. Run Pilot with Mock Data

The pilot demonstrates the complete pipeline without needing to call GitHub API:

```bash
cd /home/vaishnavkoka/RE4BDD/Mining
python run_pilot.py
```

**What the pilot does:**
- Shows sample BDD projects (cucumber-js, behave)
- Demonstrates feature file extraction
- Shows requirement mapping format
- Generates sample CSV dataset
- Displays output format and next steps

**Output:**
- `mining_outputs/bdd_oss_mining_dataset.csv` - Raw dataset
- `mining_outputs/mining_metadata.json` - Metadata and statistics

### 2. Install Dependencies (for full mining)

```bash
pip install -r mining_requirements.txt
```

### 3. Run Full Mining Pipeline

For real GitHub mining (requires internet connection):

```python
# Edit run_pilot.py or create new script:
from oss_bdd_mining import BDDMiningPipeline

pipeline = BDDMiningPipeline(use_mock_data=False)
pipeline.run_mining_pipeline()
```

**Optional: Set GitHub Token for higher API limits**

```bash
export GITHUB_TOKEN=your_github_personal_access_token
```

## Configuration

Edit `mining_config.py` to customize:

### BDD Criteria
- `min_feature_files`: Minimum 4 feature files per project (requirement)
- `feature_file_extension`: Search pattern for .feature files
- `step_definition_patterns`: Patterns for detecting step implementations

### Pilot Limits
- `max_projects_to_scan`: Number of projects to search (default: 50)
- `max_concurrent_clones`: Parallel clone operations (default: 5)
- `clone_timeout_seconds`: Time limit per clone (default: 300s)
- `max_feature_files_per_project`: Limit extraction per project (default: 20)

### Search Queries
Add or modify GitHub search queries in `GITHUB_SEARCH_QUERIES` list:
```python
GITHUB_SEARCH_QUERIES = [
    'filename:*.feature stars:>50 language:gherkin',
    'path:features/*.feature stars:>50',
    # Add more queries as needed
]
```

## CSV Dataset Format

### Columns

| Column | Description |
|--------|-------------|
| `project_id` | Unique GitHub project ID |
| `project_name` | Repository name |
| `project_url` | GitHub repository URL |
| `github_stars` | Star count (quality metric) |
| `language` | Primary language |
| `feature_file_count` | Total features in project |
| `feature_file_name` | Individual feature filename |
| `requirement_id` | Source requirement file |
| `requirement_text` | Extracted requirement (truncated) |
| `step_definitions_found` | Boolean: steps defined? |
| `step_definitions_language` | Language(s) of step files |
| `feature_file_url` | Direct link to .feature file |
| `step_definitions_url` | Link to repo |
| `mining_timestamp` | Extraction timestamp |

### Example Row
```csv
project_id,project_name,project_url,github_stars,language,feature_file_count,feature_file_name,requirement_id,requirement_text,step_definitions_found,step_definitions_language,feature_file_url,step_definitions_url,mining_timestamp
1,cucumber-js,https://github.com/cucumber/cucumber-js,2500,JavaScript,4,authentication.feature,REQUIREMENTS.md,User authentication must support...,True,javascript,https://github.com/cucumber/cucumber-js/.../authentication.feature,https://github.com/cucumber/cucumber-js,2024-03-16T10:30:00
```

## Filtering & Validation

The pipeline automatically validates projects:

✅ **Included**: Projects with ≥4 feature files
❌ **Excluded**: 
- Projects with <4 feature files
- Failed GitHub clones
- Permission/access errors

## Analysis Examples

### Load and Analyze Dataset

```python
import pandas as pd

# Load dataset
df = pd.read_csv('mining_outputs/bdd_oss_mining_dataset.csv')

# Statistics
print(f"Total projects: {df['project_id'].nunique()}")
print(f"Total features extracted: {len(df)}")
print(f"Languages: {df['step_definitions_language'].unique()}")

# Projects with step definitions
projects_with_steps = df[df['step_definitions_found'] == True]['project_name'].unique()
print(f"Projects with step definitions: {len(projects_with_steps)}")

# Requirement coverage
print(f"\nRequirement coverage:")
print(df.groupby('project_name')['requirement_id'].nunique())
```

## Troubleshooting

### GitHub API Rate Limit Exceeded
**Solution**: Set `GITHUB_TOKEN` environment variable with a personal access token

### Clone Timeout
**Solution**: Increase `clone_timeout_seconds` in mining_config.py or improve internet connection

### Permission Denied Errors
**Solution**: 
- Ensure write permissions in output directory
- Check disk space for cloning
- Re-run pipeline on cleaner directory

### No Projects Found
**Solution**:
- Verify GitHub API is accessible
- Check search queries are valid
- Ensure sufficient stars threshold in config

## Architecture

```
BDDMiningPipeline
├── search_github_projects()           # 1. Find candidates
├── clone_and_analyze_project()        # 2. Clone repo
│   ├── _extract_bdd_artifacts()
│   │   ├── _find_files()              # Find .feature files
│   │   ├── _find_step_definitions()   # Find step impl.
│   │   └── _extract_requirements()    # Extract requirements
├── generate_csv_dataset()             # 3. Create CSV
└── save_metadata()                    # 4. Save stats
```

## Extending the Pipeline

### Add New Search Query
```python
# In mining_config.py
GITHUB_SEARCH_QUERIES = [
    # ... existing queries
    'repo:my-org/* .feature',  # Add this
]
```

### Add New Language Support
```python
# In mining_config.py - step_definition_patterns
"step_definition_patterns": [
    r".*step.*\.go",      # Add Go support
    r".*spec.*\.ts",      # Add TypeScript support
]
```

### Process Results
```python
from oss_bdd_mining import BDDMiningPipeline

pipeline = BDDMiningPipeline(use_mock_data=False)
pipeline.run_mining_pipeline()

# Post-process results
for result in pipeline.mining_results:
    print(f"Project: {result['project']['name']}")
    print(f"Features: {result['feature_count']}")
```

## Metadata Output

The pipeline generates `mining_metadata.json`:

```json
{
  "timestamp": "2024-03-16T10:30:00",
  "total_projects_scanned": 50,
  "valid_projects_found": 12,
  "total_features_extracted": 48,
  "output_file": "/path/to/bdd_oss_mining_dataset.csv",
  "config": { ... }
}
```

## Key Metrics

After running the pilot or full mining, review:

1. **Total Projects Scanned**: How many repositories were analyzed
2. **Valid Projects Found**: Projects meeting ≥4 feature files criteria
3. **Total Features Extracted**: Sum of all feature files
4. **Average Features per Project**: Features / Valid Projects
5. **Language Distribution**: Breakdown by step definition language
6. **Requirement Coverage**: Features with mapped requirements

## Next Steps

1. ✅ Run pilot to validate pipeline
2. ✅ Review mock dataset format
3. 📊 Run full mining with GitHub data
4. 🔍 Analyze results and filter by criteria
5. 📈 Generate statistics and visualizations
6. 📋 Document findings in research paper

## Performance Notes

- Pilot run: <5 seconds (mock data)
- Full pilot (5 projects): ~2 minutes
- Full mining (50 projects): ~30 minutes (depends on project sizes)
- Network bandwidth: ~500MB - 1GB per full run

## Citation

If using this mining pipeline in research, please cite:

```
OSS BDD Mining Pipeline
Part of: Requirements Engineering for Behavior-Driven Development (RE4BDD)
```

## License

This mining pipeline is part of the RE4BDD research project.

## Contact & Support

For technical issues or questions about the pipeline:
1. Check logs in mining process output
2. Review mining_metadata.json for statistics
3. Verify configuration in mining_config.py
