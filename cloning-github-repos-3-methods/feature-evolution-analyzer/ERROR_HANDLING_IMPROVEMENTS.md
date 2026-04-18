# Error Handling Improvements - Feature Evolution Analyzer

## Overview
Created `enhanced_feature_evolution_analyzer_v2.py` with comprehensive error handling, debugging capabilities, and user-friendly error messages to replace cryptic errors.

## Key Improvements

### 1. **Custom Exception Classes** 
Better categorization of errors for specific handling:
- `AnalyzerError` - Base exception
- `RepositoryError` - Repository access/validation issues
- `GitOperationError` - Git-specific failures
- `NetworkError` - Network/connectivity issues
- `ValidationError` - Input validation failures
- `FileOperationError` - File I/O problems

### 2. **System Diagnostics** (`SystemDiagnostics` class)
Pre-flight checks run at startup:
```
- Platform/OS detection
- Network connectivity verification
- GitHub API availability check
- Local directory permissions check
```

**When it helps:** Immediately identifies network issues, permission problems, or environment incompatibilities before analysis starts.

### 3. **Enhanced Logging Architecture**

#### Console Logging
- All key steps logged to console with timestamps
- INFO level for important events
- DEBUG level for detailed troubleshooting (visible in log files)

#### Repository-Specific Logging
- Separate `.log` file per repository
- Complete execution history stored in output directory
- Helps diagnose failures without re-running analysis

**Log file location:**
```
evolution_analysis_results/
  ├── owner_repo1/
  │   ├── owner_repo1.log
  │   ├── owner_repo1.csv
  │   └── owner_repo1.json
  └── local_repo/
      ├── local_repo.log
      └── ...
```

### 4. **Context-Rich Error Messages**

#### Before:
```
❌ Fatal error: Repository not found
```

#### After:
```
❌ Repository Error: GitHub repository not found: owner/repo
  Verify: owner/repo name, public access
  
With context:
- Full URL being attempted
- Suggestion for resolution
- Debug information in log file
```

### 5. **Retry Logic for Network Operations**

GitHub clone operations now include:
- Configurable retry attempts (default: 3)
- Exponential backoff between retries (2 second delay)
- Specific error detection and categorization
- Automatic recovery from transient failures

```python
# Configuration in analyzer
self.max_retries = 3       # Number of retry attempts
self.retry_delay = 2       # Seconds between attempts
```

### 6. **Validation at Each Step**

#### Input Validation
- GitHub URL format validation
- Local path existence and permission checks
- CSV file structure validation ('url' column requirement)
- Empty input detection with helpful messages

#### Repository Validation
- Git repository detection (.git directory check)
- Read/write permission verification
- Path resolution (expands ~, resolves symlinks)
- Type-specific checks for GitHub vs local repos

### 7. **Comprehensive Error Handling Flow**

```
Main
  ├── Initialize Analyzer
  │   └── Run Diagnostics ← Catch init errors
  │
  ├── Get User Input
  │   └── Validate Input ← Specific error messages
  │
  ├── Parse Repositories
  │   ├── GitHub URLs ← URL format validation
  │   ├── Local Paths ← Permission/existence checks
  │   └── CSV Files ← Format/content validation
  │
  ├── Batch Analysis (per repo)
  │   ├── Clone/Open Repository ← Retry logic for network
  │   ├── Analyze Commits ← Git operation error handling
  │   └── Generate Reports ← Continue on partial failures
  │
  └── Print Summary
      └── Show detailed status per repository
```

### 8. **Stack Trace Capture**

All exceptions include:
- Exception type
- Exception message
- Full Python stack trace (in DEBUG logs)
- System diagnostics information

**Where it helps:** When contacting support or debugging, full context is available in the `.log` files.

### 9. **Graceful Degradation**

If some operations fail:
- ✓ Continues analyzing other repositories
- ✓ Generates partial reports even after errors
- ✓ Reports per-repository success/failure in summary
- ✓ Provides specific error details for each failed repo

### 10. **Better User Feedback**

#### Progress Indication
- Progress bars during commit analysis
- Clear [N/M] counter showing repository progress
- ✅/❌ symbols for visual feedback

#### Status Reporting
- Execution summary with success rate
- Per-repository status in table format
- File locations for generated outputs
- Specific error messages for failures

## Usage of Improved Version

### Running the Enhanced Version
```bash
python3 enhanced_feature_evolution_analyzer_v2.py
```

### Checking Log Files for Details
```bash
# View repository-specific log
cat evolution_analysis_results/owner_repo1/owner_repo1.log

# Search for errors
grep ERROR evolution_analysis_results/*/​*.log

# View all warnings
grep WARNING evolution_analysis_results/*/​*.log
```

### Enabling Debug Output
Debug information is automatically logged to files. To see debug output in console, modify the script:
```python
ch.setLevel(logging.DEBUG)  # Instead of logging.INFO
```

## Common Error Scenarios & Resolution

### Network Errors
**Error Message:**
```
GitOperationError: Failed to clone repository after 3 attempts
  Suggestions:
  - Check your internet connection
  - Verify the repository URL is correct
  - Check GitHub status: https://www.githubstatus.com/
```

**What to check:**
1. `connection_ok: ✗` in startup diagnostics
2. Check `.log` file for specific network errors
3. Verify GitHub is not experiencing outages

### Repository Not Found
**Error Message:**
```
RepositoryError: GitHub repository not found: owner/repo
  URL: https://github.com/owner/repo.git
  Verify: owner/repo name, public access
```

**What to check:**
1. Verify owner name is correct
2. Check repository is public (or you have access)
3. Verify spelling of repository name

### Permission Errors
**Error Message:**
```
RepositoryError: No read permission: /path/to/repo
```

**What to check:**
1. Check file permissions: `ls -la /path/to/repo`
2. Verify you own or have read access
3. Check for SELinux or AppArmor restrictions

### Invalid Input
**Error Message:**
```
ValidationError: Invalid GitHub URL format: 'invalid-url'
  Format: owner/repo or https://github.com/owner/repo
```

**What to correct:**
1. Use format: `owner/repo`
2. Or use full URL: `https://github.com/owner/repo`
3. Avoid extra characters or spaces

## Files Generated

### Per Repository
```
evolution_analysis_results/owner_repo/
├── owner_repo.log          # Complete execution history & errors
├── owner_repo.csv          # Commit timeline data
└── owner_repo.json         # Summary statistics
```

### Root Output
- Multiple repository folders with above structure
- No session folder anymore - flat structure for clarity

## Version Information

- **File:** `enhanced_feature_evolution_analyzer_v2.py`
- **Status:** Production-ready with comprehensive error handling
- **Python:** 3.6+ (tested with 3.8+)
- **Dependencies:** Same as original (git, pandas, matplotlib, gitpython)

## Recommendations

1. **Always check log files** when analysis completes
   - Look for WARN/ERROR levels
   - Review DEBUG entries if issues persist

2. **Use local repos when possible**
   - Avoids network dependencies
   - Faster analysis
   - Easier debugging

3. **Test with single repository first**
   - Verify your environment works
   - Check generated output format
   - Then batch process multiple repos

4. **Keep log files for reference**
   - Useful for debugging
   - Historical record of analyses
   - Can be deleted after verification if needed

## Migration from Original Version

The new version is fully backward compatible:
- Same input modes (GitHub/Local/CSV)
- Same output format (CSV/JSON/PNG)
- Same command-line experience
- But with better error messages and logging

To use: Simply replace the filename with `enhanced_feature_evolution_analyzer_v2.py`.

## Future Improvements

Potential enhancements:
- [ ] Configuration file support (retry counts, timeouts)
- [ ] JSON output for programmatic access to errors
- [ ] Email notifications for failures
- [ ] Automatic log rotation
- [ ] Performance metrics per repository
- [ ] Batch error recovery without re-running
