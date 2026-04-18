# Quick Start - Enhanced Error Handling Version

## What's New

The new `enhanced_feature_evolution_analyzer_v2.py` provides:

### ✅ Better Error Messages
Instead of "Fatal error: Repository not found", you get:
```
RepositoryError: GitHub repository not found: owner/repo
  URL: https://github.com/owner/repo.git
  Verify: owner/repo name, public access
```

### ✅ System Diagnostics
Checks at startup:
- Is your network connected?
- Can you reach GitHub API?
- Do you have write permissions?

### ✅ Detailed Logs
Every repository analysis creates a `.log` file with:
- Complete execution timeline
- All errors with context
- Debug information for troubleshooting

###  ✅ Retry Logic
Network failures automatically retry (3 attempts by default)

### ✅ Graceful Failures
If one repository fails, others still process

## Running It

```bash
# Navigate to the directory
cd /path/to/feature-evolution-analyzer

# Run the new version
python3 enhanced_feature_evolution_analyzer_v2.py
```

## Input Modes

### 1️⃣ GitHub URLs
```
Enter: owner/repo
Or:    https://github.com/owner/repo
```

For multiple: comma-separated
```
owner/repo1, owner/repo2, owner/repo3
```

### 2️⃣ Local Paths
```
Enter: /path/to/local/repo
```

For multiple: comma-separated
```
/path/repo1, /path/repo2
```

### 3️⃣ CSV File
```
Enter: repositories.csv
```

CSV format:
```
url
https://github.com/owner/repo1
https://github.com/owner/repo2
owner/repo3
```

## Output Files

After analysis, check: `evolution_analysis_results/`

```
evolution_analysis_results/
├── owner_repo1/
│   ├── owner_repo1.log   ← Check if errors occurred
│   ├── owner_repo1.csv   ← Commit timeline
│   └── owner_repo1.json  ← Summary stats
│
└── owner_repo2/
    ├── owner_repo2.log
    ├── owner_repo2.csv
    └── owner_repo2.json
```

## Checking Results

### View Summary
```bash
# After analysis completes, check the summary printed
# Shows success/failure count, output locations
```

### View Detailed Logs
```bash
# View log for a specific repository
cat evolution_analysis_results/owner_repo1/owner_repo1.log

# View only errors
grep ERROR evolution_analysis_results/owner_repo1/owner_repo1.log

# View only warnings
grep WARNING evolution_analysis_results/owner_repo1/owner_repo1.log

# View full debug output
grep -E "DEBUG|INFO|ERROR" evolution_analysis_results/*/​*.log
```

### View Data
```bash
# Open CSV in spreadsheet app or command line
head evolution_analysis_results/owner_repo1/owner_repo1.csv

# View JSON summary
cat evolution_analysis_results/owner_repo1/owner_repo1.json | python3 -m json.tool
```

## Troubleshooting

### "❌ No repositories found"
**Causes:**
- Invalid URL format
- Non-existent local path
- Empty CSV file

**Solution:**
- Check format of input (owner/repo or https://github.com/owner/repo)
- Verify local paths exist with `ls -la`
- Ensure CSV has 'url' column

### "❌ Repository Error: Not a git repository"
**Causes:**
- Path doesn't have `.git` folder
- Wrong directory provided

**Solution:**
- Navigate to correct repository
- Verify `.git` folder exists: `ls -la` should show `.git`

### "⚠️  Connection error, retry in 2s..."
**Causes:**
- Network connectivity issue
- GitHub temporarily unreachable
- Local machine is offline

**Solution:**
- Check internet connection
- Try again later if GitHub is down
- Check: https://www.githubstatus.com/

### "❌ Repository not found: owner/repo"
**Causes:**
- Wrong owner/repo name
- Repository is private (and you don't have access)
- Typo in repository name

**Solution:**
- Verify spelling and capitalization
- Check if it's a private repo you need SSH access for
- Use `https://github.com/owner/repo` URL to double-check

## Features Comparison

| Feature | Original | Enhanced v2 |
|---------|----------|------------|
| Basic analysis | ✓ | ✓ |
| Console output | ✓ | ✓ |
| CSV/JSON reports | ✓ | ✓ |
| Log files | Basic | **Detailed** |
| Error messages | Generic | **Context-rich** |
| Network retry | ✗ | **✓ (3 attempts)** |
| Startup diagnostics | ✗ | **✓** |
| Debug logging | ✗ | **✓** |
| Error classification | ✗ | **5 types** |
| Continue on error | Partial | **Improved** |

## Common Success Scenarios

### Single Repository
```bash
python3 enhanced_feature_evolution_analyzer_v2.py

# Input: GitHub URLs
# Enter URL: owner/repo

# File tracking mode: Feature Files Only (1)

# Results:
# ✅ owner_repo completed
# Output: evolution_analysis_results/owner_repo/
```

### Multiple Repositories
```bash
python3 enhanced_feature_evolution_analyzer_v2.py

# Input: GitHub URLs  
# Enter URL: owner/repo1, owner/repo2, owner/repo3

# File tracking mode: All Files (2)

# Results:
# ✅ owner_repo1 completed
# ✅ owner_repo2 completed
# ❌ owner_repo3 failed (details in log)
# Summary: 2/3 successful
```

### Batch from CSV
```bash
# First create repos.csv
cat > repos.csv << EOF
url
https://github.com/owner1/repo1
https://github.com/owner2/repo2
owner3/repo3
EOF

# Run analyzer
python3 enhanced_feature_evolution_analyzer_v2.py

# Input: CSV File
# Enter path: repos.csv

# Results process all 3 repos
```

## Performance Tips

1. **Start with one repo** to test
2. **Use local paths** when possible (no network latency)
3. **Choose "Feature Files Only"** for faster processing
4. **Process during off-hours** for large batches

## Getting Help

If you encounter an error:

1. **Read the error message** - it now includes suggestions
2. **Check the log file** - contains full debug info
3. **Look at the status diagnostics** - at startup shows network status
4. **Note the exact error** - when seeking help or reporting issues

## Version Info

- **File:** `enhanced_feature_evolution_analyzer_v2.py`
- **Status:** Ready to use
- **Python:** 3.6+ (tested with 3.8+)
- **Requires:** git, pandas, numpy, matplotlib, gitpython

## Need More Info?

See: `ERROR_HANDLING_IMPROVEMENTS.md` for comprehensive documentation
