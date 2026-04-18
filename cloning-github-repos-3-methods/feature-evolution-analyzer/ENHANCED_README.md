# Enhanced Feature File Evolution Analyzer

A powerful tool to analyze how BDD `.feature` files evolve over time in GitHub repositories. Supports multiple input modes, comprehensive logging, and beautiful visualizations.

## 🎯 Features

✅ **Multiple Input Modes**
- GitHub Repository URLs (single or multiple)
- Local Repository Paths (already cloned)
- CSV Files (batch processing with metadata)

✅ **Core Capabilities**
- Analyzes entire git commit history
- Tracks feature file creation, modification, deletion
- Generates commit-by-commit timeline (CSV)
- Creates statistical summaries (JSON)
- Produces beautiful visualizations (PNG charts)
- Single unified progress bar using tqdm

✅ **Robust Error Handling**
- API failure recovery
- Connection error handling
- Graceful error logging
- Detailed error messages

✅ **Comprehensive Logging**
- File logging (detailed debug info)
- Console logging (user-friendly info)
- Separate log file per session
- Timestamp for all operations

✅ **Execution Summary**
- Repository-wise statistics
- Success/failure breakdown
- Execution duration tracking
- Detailed summary report

## 📋 Prerequisites

```bash
# Required
- Python 3.7+
- Git
- Internet connection (for GitHub mode)
```

## 🚀 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Method 1: Interactive CLI (Recommended)

```bash
python3 enhanced_feature_evolution_analyzer.py
```

The script will guide you through:

1. **Select Input Mode:**
   ```
   1. GitHub Repository URL(s)
   2. Local Repository Path(s)
   3. CSV File with Metadata
   ```

2. **Provide Input:**
   - GitHub: `cucumber/gherkin` or `https://github.com/cucumber/gherkin`
   - Local: `/path/to/repo` or `/path/repo1, /path/repo2`
   - CSV: `path/to/repositories.csv`

### Method 2: GitHub URL Mode

```bash
# Single repository
python3 enhanced_feature_evolution_analyzer.py

# Then choose option 1 and enter:
# cucumber/gherkin
```

Or with multiple repos:
```
# Enter multiple URLs separated by commas:
# cucumber/gherkin, behave/behave, cucumber/cucumber-ruby
```

### Method 3: Local Repository Mode

```bash
# Choose option 2 and enter:
# /home/user/repos/my-bdd-project
```

Or with multiple local repos:
```
# /home/user/repos/repo1, /home/user/repos/repo2
```

### Method 4: CSV Batch Mode

Prepare a CSV file `repositories.csv`:
```csv
url,description,team
cucumber/gherkin,Gherkin parser,Core
cucumber/cucumber-ruby,Ruby implementation,Core
behave/behave,Python framework,Tools
```

```bash
# Choose option 3 and enter:
# repositories.csv
```

## 📊 Output Files

Each analysis session creates `evolution_analysis_results/session_YYYYMMDD_HHMMSS/` with:

### Per-Repository Output
```
analysis_repo_name_YYYYMMDD_HHMMSS/
├── repo_clone/                           # Git repository (optional)
├── evolution_timeline.csv               # Commit-by-commit timeline
├── evolution_stats.json                 # Statistical summary
└── evolution_visualization.png          # 4-panel chart
```

### Session-Level
```
evolution_analysis_results/
└── session_YYYYMMDD_HHMMSS/
    ├── evolution_analysis_YYYYMMDD_HHMMSS.log  # Detailed log file
    ├── analysis_repo1_YYYYMMDD_HHMMSS/
    ├── analysis_repo2_YYYYMMDD_HHMMSS/
    └── ...
```

## 📄 Output File Details

### 1. `evolution_timeline.csv`
Commit-by-commit timeline:
```csv
Commit,Date,Author,Feature Files,Total Lines
3c1d4f,2017-01-08 14:23:45,Author Name,35,426
2a8b9e,2017-01-09 10:15:30,Author Name,36,500
7f2c3d,2017-01-10 16:45:12,Author Name,36,480
```

**Use for:** Detailed timeline analysis, charting, data science

### 2. `evolution_stats.json`
Statistical summary:
```json
{
  "repository": "cucumber/gherkin",
  "total_commits": 3545,
  "feature_files_created": 607,
  "feature_files_current": 105,
  "total_lines_current": 4908,
  "average_growth": 1.26
}
```

**Use for:** Comparison, quick metrics, dashboards

### 3. `evolution_visualization.png`
4-panel chart showing:
- **Panel 1:** Feature files count over time
- **Panel 2:** Total lines of code over time
- **Panel 3:** Growth rate with moving average
- **Panel 4:** Statistics summary box

**Use for:** Reports, presentations, visualization

### 4. `evolution_analysis_YYYYMMDD_HHMMSS.log`
Detailed session log:
```
2026-04-13 19:30:45 - INFO - Selected input mode: github
2026-04-13 19:30:46 - INFO - GitHub input received: 2 repo(s)
2026-04-13 19:30:47 - DEBUG - Parsed GitHub repo: cucumber/gherkin
2026-04-13 19:30:48 - INFO - Starting analysis: gherkin
2026-04-13 19:30:49 - DEBUG - Cloning from: https://github.com/cucumber/gherkin.git
...
2026-04-13 19:45:30 - INFO - ✅ Successfully analyzed: gherkin
2026-04-13 19:45:31 - INFO - Parsed 2 repositories
```

**Use for:** Debugging, auditing, troubleshooting

## 🔍 Key Metrics Explained

| Metric | Description | Insight |
|--------|-------------|---------|
| **Feature Files Created** | Total unique feature files ever created | Project scope |
| **Feature Files Current** | Feature files in latest commit | Current state |
| **Total Lines** | Total lines of code in all feature files | Test coverage scale |
| **Average Growth** | Lines added per commit on average | Development velocity |
| **Total Commits** | Commits touching feature files | Activity level |

## 📈 Example: Interpreting Results

### Growing Project Pattern
```
Features: 35 → 600
Lines: 426 → 30,000
Pattern: Stead growth = Active development
Implication: Project is expanding features continuously
```

### Mature Project Pattern
```
Features: 600 → 300 (cleaned)
Lines: 30,000 → 5,000 (consolidated)
Pattern: Plateau then decline = Consolidation
Implication: Project matured, now focusing on quality over quantity
```

### Stable Project Pattern
```
Features: 100 → 105
Lines: 5,000 → 5,500
Pattern: Flat line = Maintenance mode
Implication: Project is stable, adding minimal new tests
```

## 🛠️ Error Handling

### GitHub Connection Error
```
❌ Connection error while cloning
→ Check internet connection
→ Verify GitHub is accessible
→ Repository is public or credentials configured
```

### Repository Not Found
```
❌ Repository not found: https://github.com/owner/repo
→ Check repository URL
→ Verify repository exists
→ Ensure repository is public
```

### Invalid Local Path
```
❌ Path does not exist: /path/to/repo
→ Verify path is correct
→ Ensure path has .git directory
```

### CSV Errors
```
❌ CSV must have 'url' column
→ Add 'url' column to CSV
→ Ensure proper column naming
```

## 📝 Logging

### Log Levels
- **DEBUG:** Detailed technical information
- **INFO:** General progress information
- **WARNING:** Non-critical issues
- **ERROR:** Critical failures

### Log File Location
```
evolution_analysis_results/
└── session_YYYYMMDD_HHMMSS/
    └── evolution_analysis_YYYYMMDD_HHMMSS.log
```

### View Logs
```bash
# Latest session log
tail -f evolution_analysis_results/session_*/evolution_analysis_*.log

# Specific session
cat evolution_analysis_results/session_20260413_193045/evolution_analysis_20260413_193045.log
```

## 🎯 Progress Tracking

### Single Unified Progress Bar
```
Analyzing commits: 45%|████▌     | 1600/3545 [05:30<06:45, 2.17 commit/s]
```

Shows:
- Percentage completion
- Items processed / Total items
- Time elapsed and ETA
- Processing speed

## 📊 Execution Summary

After completion, you'll see:
```
======================================================================
📊 EXECUTION SUMMARY
======================================================================

✅ Session Directory: evolution_analysis_results/session_20260413_193045

📈 Repositories Analyzed:
   • Total: 2
   • Successful: 2
   • Failed: 0

📊 Success Rate: 100.0%

⏱️  Duration: 0:15:30

Repository Details:
  ✅ gherkin: 3545 commits analyzed
  ✅ behave: 2891 commits analyzed

======================================================================
```

## 🚨 Troubleshooting

### Issue: "Repository not found"
**Solution:**
- Check URL spelling
- Ensure repository is public
- Verify GitHub is accessible

### Issue: Clone takes too much time
**Solution:**
- Uses `--depth=1` for faster cloning
- Large repos may take time anyway
- Check internet connection speed

### Issue: Out of memory on large repos
**Solution:**
- Analyze one repository at a time
- Increase swap space
- Use local path instead of cloning

### Issue: Permission denied
**Solution:**
```bash
# Ensure directory is writable
chmod 755 evolution_analysis_results/

# For local repos
chmod 755 /path/to/repo
```

## 💡 Tips & Best Practices

1. **Batch Processing:** Use CSV mode for analyzing 10+ repositories
2. **Local Analysis:** Use local path mode if repos already cloned (faster)
3. **Large Repos:** Analyze separately to avoid memory issues
4. **CSV Format:** Include metadata columns for better tracking
5. **Log Review:** Check logs for warnings before publishing results

## 📦 Sample CSV Format

```csv
url,project_name,team,language
cucumber/gherkin,Gherkin Parser,Core,Multi
cucumber/cucumber-ruby,Ruby Impl,Core,Ruby
behave/behave,Python BDD,Community,Python
jestjs/jest,Jest,Tools,JavaScript
```

## 🔗 Integration with Repository Cloner

This analyzer pairs perfectly with the BDD Repository Cloner:

```bash
# 1. Clone 51 repositories
python3 clone_bdd_repos_seart_tool-1.py

# 2. Analyze all cloned repos
python3 enhanced_feature_evolution_analyzer.py
# → Select option 2 (Local paths)
# → Point to cloned_repos directory

# 3. Get comprehensive analysis of entire ecosystem
```

## 📄 License

MIT

---

**Last Updated:** April 2026  
**Status:** ✅ Production Ready  
**Tested on:** Python 3.7+, Linux/macOS/Windows
