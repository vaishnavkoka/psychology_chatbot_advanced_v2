# BDD Repository Cloner with Checkpoint Support

A comprehensive Python utility to clone Behavior-Driven Development (BDD) repositories from GitHub with advanced features including checkpoint resumption, logging, and detailed statistics.

## 🎯 Features

- ✅ **Smart Filtering** - Only clones repositories with feature_count ≥ 10
- ✅ **Checkpoint System** - Resume from last processed repository if interrupted
- ✅ **Progress Tracking** - Single unified progress bar using tqdm
- ✅ **Comprehensive Logging** - Timestamped logs of all actions
- ✅ **Error Handling** - Graceful handling of connection issues and failures
- ✅ **Connection Check** - Verifies GitHub connectivity before starting
- ✅ **Detailed Statistics** - JSON output with execution summary
- ✅ **Shallow Cloning** - Uses `--depth=1` for faster cloning
- ✅ **Skip Tracking** - Records all skipped repositories with reasons
- ✅ **Timeout Protection** - 60-second timeout per clone operation

## 📊 Current Dataset Statistics

```
Total repositories:        1,628
Eligible (≥10 features):     51  (3.1%)
To be skipped:           1,577  (96.9%)
```

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Python 3.7+
- Git
- Internet connection to GitHub
- ~2-5 GB disk space (depending on repo sizes)
```

### Installation

```bash
cd /path/to/seart-tool-1-cloned-repos
# No additional packages needed beyond Python standard library + tqdm
pip install tqdm  # Already likely installed
```

### Basic Run - Interactive Mode

```bash
python3 clone_bdd_repos_seart_tool-1.py
```

The script will prompt you for a folder name:

```
======================================================================
🚀 BDD Repository Cloner - Initialization
======================================================================

Enter folder name for cloned repositories [cloned_repos]: 
```

- **Press Enter** to use the default: `cloned_repos`
- **Type a custom name** to organize multiple cloning sessions

Example with custom folder:
```bash
$ python3 clone_bdd_repos_seart_tool-1.py
Enter folder name for cloned repositories [cloned_repos]: my_research_project

✅ Folder name set to: my_research_project
✅ Checkpoint file: .my_research_project_checkpoint.json
✅ Log file: my_research_project_execution_20260413_184520.log
```

### Resume from Checkpoint

If execution is interrupted:
```bash
# Simply run the same command again
python3 clone_bdd_repos_seart_tool-1.py

# You'll be prompted for folder name (enter the same name to resume)
Enter folder name for cloned repositories [cloned_repos]: my_research_project

📋 Checkpoint loaded - Resuming from: 50 repos processed (30 ✅, 15 ⏭️, 5 ❌)
Repository Processing: 100%|██████████| 1628/1628 [continuing...]
```

**Note**: The checkpoint is folder-specific. Multiple cloning sessions with different folder names run independently without interference.

## 📁 Output Structure

Output files are dynamically named based on the folder name you provide at startup:

### With Default Folder Name (`cloned_repos`)
```
seart-tool-1-cloned-repos/
├── clone_bdd_repos_seart_tool-1.py                       # This script
├── CLONER_README.md                                      # This file
├── seart-search-repos-consolidated-removed-duplicates-sorted-output.csv
│
├── cloned_repos/                                         # Output directory (your choice)
│   ├── repo-1-name/
│   ├── repo-2-name/
│   └── ...
│
├── .cloned_repos_checkpoint.json                         # Checkpoint (folder-specific)
├── cloned_repos_execution_20260413_184520.log            # Execution log
└── cloned_repos_statistics_20260413_184520.json          # Statistics summary
```

### With Custom Folder Name (`my_research_project`)
```
seart-tool-1-cloned-repos/
├── my_research_project/                                  # Your custom folder
│   ├── repo-1-name/
│   ├── repo-2-name/
│   └── ...
│
├── .my_research_project_checkpoint.json                  # Checkpoint (folder-specific)
├── my_research_project_execution_20260413_184520.log     # Execution log
└── my_research_project_statistics_20260413_184520.json   # Statistics summary
```

**Multiple Sessions**: Each folder name gets its own checkpoint and logs, allowing you to run multiple cloning operations in parallel without interference.

## 📋 Configuration

### Runtime Configuration (Interactive)

When you run the script, you'll be asked for the folder name:

```
Enter folder name for cloned repositories [cloned_repos]: 
```

- **Folder name**: User-provided at startup (default: `cloned_repos`)
- **Checkpoint file**: `.{folder_name}_checkpoint.json`
- **Log file**: `{folder_name}_execution_YYYYMMDD_HHMMSS.log`
- **Stats file**: `{folder_name}_statistics_YYYYMMDD_HHMMSS.json`

All files and folders are dynamically created based on your choice, allowing multiple concurrent cloning operations.

### Code Configuration (Advanced)

Edit these constants in `clone_bdd_repos_seart_tool-1.py` if needed:

```python
CSV_FILE = "seart-search-repos-consolidated-removed-duplicates-sorted-output.csv"
MIN_FEATURE_COUNT = 10                               # Minimum .feature files to clone
```

### Examples

**Change minimum feature count:**
```python
MIN_FEATURE_COUNT = 20  # Clone only repos with ≥20 features
```

**Use different CSV file:**
```python
CSV_FILE = "my_custom_repos.csv"  # Must have 'github_url' and 'feature_count' columns
```

## 🔄 Execution Flow

```
┌─────────────────────────────────────┐
│ 1. Connection Check                  │ ← Verify GitHub connectivity
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 2. Setup                             │ ← Create output directory
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 3. Load CSV & Checkpoint             │ ← Resume from checkpoint if exists
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 4. Process Each Repository           │ ← Single progress bar
├─────────────────────────────────────┤
│ For each repo:                       │
│ • Check feature_count                │
│ • If >= 10: Clone                    │
│ • If < 10: Skip & record             │
│ • Update progress & checkpoint       │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 5. Generate Statistics               │ ← JSON summary file
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 6. Print Summary Report              │ ← Console output
└─────────────────────────────────────┘
```

## 📊 Checkpoint System

### How It Works

- **Auto-saved** every 5 repositories processed
- **JSON format** with processed row indices, execution statistics, and timestamp
- **Resumable** - next run automatically loads and skips already-processed repos
- **Preserved** even if user cancels (Ctrl+C)
- **Folder-specific** - each folder name maintains its own checkpoint

### Enhanced Checkpoint File Example

The checkpoint now saves detailed statistics for better resumption messaging:

```json
{
  "processed_rows": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
  "statistics": {
    "total_processed": 10,
    "successfully_cloned": 6,
    "skipped": 3,
    "errors": 1
  },
  "timestamp": "2026-04-13T18:45:23.123456"
}
```

### Resume Messaging

When resuming from checkpoint, you'll see:

```
📋 Checkpoint loaded - Resuming from: 50 repos processed (30 ✅, 15 ⏭️, 5 ❌)
```

This shows:
- **30 ✅**: Already successfully cloned
- **15 ⏭️**: Already skipped (feature_count < 10)
- **5 ❌**: Previously encountered errors

### Reset Checkpoint

To start fresh (discard checkpoint):

```bash
# For default folder:
rm .cloned_repos_checkpoint.json

# For custom folder:
rm ".{folder_name}_checkpoint.json"

# Then run normally
python3 clone_bdd_repos_seart_tool-1.py
```

## 📝 Logging

### Log Files

- **File**: `clone_execution_YYYYMMDD_HHMMSS.log`
- **Format**: `TIMESTAMP - LEVEL - MESSAGE`
- **Levels**: INFO, WARNING, ERROR, DEBUG

### Sample Log Output

```
2026-04-13 18:45:20,123 - INFO - ======================================================================
2026-04-13 18:45:20,124 - INFO - 🚀 BDD Repository Cloner started
2026-04-13 18:45:20,125 - INFO - ======================================================================
2026-04-13 18:45:20,200 - INFO - 🔍 Checking connection to GitHub...
2026-04-13 18:45:20,456 - INFO - ✅ Connection to GitHub established successfully
2026-04-13 18:45:20,500 - INFO - ✅ Created/verified output directory: cloned_repos
2026-04-13 18:45:20,600 - INFO - 📖 CSV file loaded: 1628 total repositories
2026-04-13 18:45:20,700 - INFO - ⏭️  Repository already cloned: repo-1-name
2026-04-13 18:45:21,200 - INFO - ✅ Successfully cloned: repo-2-name
```

### Log Levels

- **✅ INFO** - Successful operations, progress updates
- **⚠️  WARNING** - Non-fatal issues, skips
- **❌ ERROR** - Failures that don't stop execution
- **🔄 DEBUG** - Detailed operation information (optional)

## 📊 Statistics Report

### Statistics File

- **File**: `clone_statistics_YYYYMMDD_HHMMSS.json`
- **Format**: Comprehensive JSON with all execution metrics
- **Updated**: Only at end of execution

### Statistics Example

```json
{
  "total_repos": 1628,
  "processed": 1628,
  "cloned": 51,
  "skipped": 1577,
  "errors": 0,
  "start_time": "2026-04-13T18:45:20.123456",
  "end_time": "2026-04-13T19:30:45.987654",
  "cloned_repos": [
    {
      "sno": 1,
      "url": "https://github.com/cucumber-school/bdd-with-cucumber",
      "feature_count": 538,
      "repo_name": "bdd-with-cucumber"
    }
  ],
  "skipped_repos": [
    {
      "sno": 5,
      "url": "https://github.com/some-repo",
      "feature_count": 8,
      "reason": "feature_count < 10"
    }
  ],
  "failed_repos": [
    {
      "sno": 10,
      "url": "https://github.com/private-repo",
      "feature_count": 50,
      "error": "Remote repository not found"
    }
  ]
}
```

## 🔍 Progress Bar

The script displays a single comprehensive progress bar:

```
Repository Processing: 45%|████▌     | 750/1628 [05:30<06:45, 2.17 repo/s]
Cloned: 23, Skipped: 725, Errors: 2
```

**Metrics shown:**
- `Cloned` - Successfully cloned repositories
- `Skipped` - Repositories not meeting criteria
- `Errors` - Failed clone operations

## ⚠️ Error Handling

### Common Errors & Solutions

**Error: "Connection failed to GitHub"**
```
Cause: No internet or GitHub is unreachable
Solution: Check internet connection and try again
```

**Error: "Remote repository not found"**
```
Cause: Repository was deleted or made private
Solution: Automatically skipped, execution continues
```

**Error: "Clone timeout (60s)"**
```
Cause: Repository too large or network slow
Solution: Automatically retried on next resumption
```

**Error: "Directory already exists"**
```
Cause: Repository was previously cloned
Solution: Automatically detected, skipped
```

### Error Recovery

The script handles errors gracefully:

1. **Non-fatal errors** → Logged and execution continues
2. **Interrupted execution** → Checkpoint saved, resume with same command
3. **Connection loss** → Fails cleanly with checkpoint preservation

## 🎯 Usage Examples

### Example 1: Basic Execution with Default Folder

```bash
$ python3 clone_bdd_repos_seart_tool-1.py

======================================================================
🚀 BDD Repository Cloner - Initialization
======================================================================

Enter folder name for cloned repositories [cloned_repos]: 
✅ Folder name set to: cloned_repos
✅ Checkpoint file: .cloned_repos_checkpoint.json
✅ Log file: cloned_repos_execution_20260413_184520.log

======================================================================

Repository Processing: 100%|██████████| 1628/1628 [45:23<00:00, 0.60 repo/s]
Cloned: 51, Skipped: 1577, Errors: 0

======================================================================
📊 EXECUTION SUMMARY
======================================================================
Total Repositories: 1628
Processed: 1628
✅ Cloned: 51
⏭️  Skipped: 1577
⚠️  Errors: 0
📁 Clone Directory: cloned_repos
📋 Checkpoint File: .cloned_repos_checkpoint.json
📊 Statistics File: cloned_repos_statistics_20260413_184520.json
======================================================================
✅ Execution completed successfully
======================================================================
```

### Example 2: Custom Folder Name

```bash
$ python3 clone_bdd_repos_seart_tool-1.py

Enter folder name for cloned repositories [cloned_repos]: my_research_analysis
✅ Folder name set to: my_research_analysis
✅ Checkpoint file: .my_research_analysis_checkpoint.json
✅ Log file: my_research_analysis_execution_20260413_190000.log

======================================================================
[Cloning proceeds with custom folder]
...
```

### Example 3: Resume from Checkpoint

```bash
# First run (interrupted after 30 minutes):
$ python3 clone_bdd_repos_seart_tool-1.py
Enter folder name for cloned repositories [cloned_repos]: 
Repository Processing: 45%|████▌     | 750/1628 [30:00<40:00, ...]
[User presses Ctrl+C - checkpoint saved]

# Next day, resume:
$ python3 clone_bdd_repos_seart_tool-1.py
Enter folder name for cloned repositories [cloned_repos]: 

📋 Checkpoint loaded - Resuming from: 750 repos processed (45 ✅, 700 ⏭️, 5 ❌)
Repository Processing: 100%|██████████| 1628/1628 [25:13<00:00, 1.08 repo/s]
Cloned: 51, Skipped: 1577, Errors: 0
[Completed successfully with only remaining repos processed]
```

### Example 4: Multiple Concurrent Sessions

```bash
# Terminal 1: Research project A
$ python3 clone_bdd_repos_seart_tool-1.py
Enter folder name for cloned repositories [cloned_repos]: project_a

# Terminal 2: Research project B (same machine, different folder)
$ python3 clone_bdd_repos_seart_tool-1.py
Enter folder name for cloned repositories [cloned_repos]: project_b

# Both operations run independently with separate checkpoints:
# - .project_a_checkpoint.json
# - .project_b_checkpoint.json
# - project_a/ and project_b/ folders
```

### Example 5: View Cloned Repos

```bash
# List successfully cloned repositories
$ ls -lh cloned_repos/ | head -10
dr-xr-xr-x  8 user  group  256 Apr 13 18:55 bdd-with-cucumber
dr-xr-xr-x  6 user  group  192 Apr 13 18:58 playwright-bdd
dr-xr-xr-x  4 user  group  128 Apr 13 19:00 gherkin-lint
...
```

## 🎓 Understanding the Output

### Log Messages

```
✅  = Operation succeeded (INFO)
⏭️  = Operation skipped (INFO)
⚠️  = Operation warning (WARNING)
❌  = Operation failed (ERROR)
🔍  = Connection check
💾  = Checkpoint save
📋  = File operations
📊  = Statistics operations
🚀  = Process start/end
📁  = Directory operations
🔄  = Clone operation
📖  = CSV read operation
```

## 🔧 Advanced Usage

### Modify Feature Count Threshold

Edit `clone_bdd_repos.py`:

```python
MIN_FEATURE_COUNT = 50  # Only clone repos with 50+ features
```

### Use Custom CSV File

```python
CSV_FILE = "my_custom_repos.csv"  # Must have 'github_url' and 'feature_count' columns
```

### Use Different Output Directory

```python
CLONED_REPOS_DIR = "/mnt/external_drive/my_repos"
```

## 📈 Performance Expectations

### Cloning Speed

- **Per repo**: 3-15 seconds average (with --depth=1)
- **Network dependent**: Varies by repo size and connection speed
- **51 eligible repos**: ~3-8 hours total for full dataset

### Disk Space

- **Average repo size**: 50-500 MB
- **Total estimated**: 2-5 GB for 51 repos
- **Depends on**: Repository history and file sizes

### Resource Usage

- **CPU**: Minimal (git I/O bounded)
- **Memory**: ~100 MB for script + OS buffer cache
- **Network**: ~30-100 Mbps during clones

## 🐛 Troubleshooting

### Issue: Progress bar seems stuck

**Solution**: 
```bash
# Check if git is running in background
ps aux | grep git
# Check log file for details
tail -f clone_execution_*.log
```

### Issue: "tqdm not found"

**Solution:**
```bash
pip install tqdm
```

### Issue: Permission denied on clone directory

**Solution:**
```bash
chmod 755 cloned_repos/
# Or, change output directory to writable location
# Edit clone_bdd_repos.py and modify CLONED_REPOS_DIR
```

### Issue: "Git command not found"

**Solution:**
```bash
# Install git
sudo apt-get install git  # Ubuntu/Debian
brew install git          # macOS
# Or use official installer from git-scm.com
```

## 📞 Support

For issues or questions:

1. Check execution log: `clone_execution_*.log`
2. Review statistics: `clone_statistics_*.json`
3. Verify checkpoint: `cat .clone_checkpoint.json`
4. Ensure prerequisites installed: `git --version && python3 --version`

## 📄 License

This utility is open source and available for use.

---

**Last Updated**: April 2026  
**Status**: ✅ Production Ready  
**Tested on**: Python 3.7+, Ubuntu/Linux, macOS
