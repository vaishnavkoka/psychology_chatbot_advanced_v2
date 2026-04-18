#!/usr/bin/env python3
"""
Usage Examples for Enhanced Feature Evolution Analyzer

This script demonstrates how to use the analyzer with different input modes.
"""

print("""
╔════════════════════════════════════════════════════════════════════════╗
║        Enhanced Feature File Evolution Analyzer - Usage Guide          ║
╚════════════════════════════════════════════════════════════════════════╝

📚 QUICK START
═══════════════════════════════════════════════════════════════════════════

1️⃣  INSTALL DEPENDENCIES
   
   $ pip install -r requirements.txt

2️⃣  RUN THE ANALYZER

   $ python3 enhanced_feature_evolution_analyzer.py


🔧 INPUT MODE 1: GITHUB REPOSITORY URLs
═══════════════════════════════════════════════════════════════════════════

Choose option 1 at the prompt, then enter:

✓ SINGLE REPOSITORY
  👉 Enter URL(s): cucumber/gherkin
  
  Or longer format:
  👉 Enter URL(s): https://github.com/cucumber/gherkin
  
  Or SSH format:  
  👉 Enter URL(s): git@github.com:cucumber/gherkin.git

✓ MULTIPLE REPOSITORIES (comma-separated)
  👉 Enter URL(s): cucumber/gherkin,behave/behave,cucumber/cucumber-ruby
  
  The analyzer will:
  • Clone each repository
  • Analyze all commits
  • Generate reports for each
  • Summary statistics at end


📂 INPUT MODE 2: LOCAL REPOSITORY PATHS
═══════════════════════════════════════════════════════════════════════════

Choose option 2 at the prompt, then enter:

✓ SINGLE LOCAL REPOSITORY
  👉 Enter path(s): /home/user/repos/my-bdd-project
  
  Or relative path:
  👉 Enter path(s): ./my-bdd-project

✓ MULTIPLE LOCAL REPOSITORIES (comma-separated)
  👉 Enter path(s): /home/user/repos/repo1,/home/user/repos/repo2
  
  The analyzer will:
  • Use existing git history (no clone needed - faster!)
  • Analyze all commits
  • Generate reports
  • Summary statistics


📊 INPUT MODE 3: CSV FILE (Batch Processing)
═══════════════════════════════════════════════════════════════════════════

Create a CSV file (e.g., repositories.csv):

  url,description,team,language
  cucumber/gherkin,Gherkin parser,Core,Multi
  cucumber/cucumber-ruby,Ruby implementation,Core,Ruby
  behave/behave,Python framework,Community,Python
  cucumber/cucumber-jvm,Java implementation,Core,Java

Then choose option 3 and enter:
  👉 Enter CSV file path: repositories.csv

The analyzer will:
  • Read all URLs from 'url' column
  • Preserve all metadata (description, team, language)
  • Analyze each repository
  • Skip invalid URLs with warnings
  • Generate combined analysis


📈 UNDERSTANDING THE OUTPUT
═══════════════════════════════════════════════════════════════════════════

After analysis, you'll get:

  evolution_analysis_results/
  └── session_20260413_193045/                    
      ├── evolution_analysis_20260413_193045.log   ← Detailed logs
      ├── analysis_gherkin_20260413_193045/
      │   ├── repo_clone/                          ← Source code (optional)
      │   ├── evolution_timeline.csv               ← Commit-by-commit data
      │   ├── evolution_stats.json                 ← Summary metrics
      │   └── evolution_visualization.png          ← 4-panel chart
      ├── analysis_behave_20260413_193045/
      │   ├── evolution_timeline.csv
      │   ├── evolution_stats.json
      │   └── evolution_visualization.png
      └── ...

📋 FILES EXPLAINED:

  evolution_timeline.csv
    → Raw data with one row per commit
    → Shows feature count and lines count at each commit
    → Good for time-series analysis

  evolution_stats.json
    → Statistical summary
    → Total commits, feature files created, current state
    → Quick overview of repository health

  evolution_visualization.png
    → 4-panel chart:
      1. Feature files count over time
      2. Total lines of code over time
      3. Growth rate with moving average
      4. Summary statistics

  evolution_analysis.log
    → Complete operation log
    → DEBUG level for debugging
    → INFO/ERROR for key events


🎯 REAL-WORLD EXAMPLES
═══════════════════════════════════════════════════════════════════════════

EXAMPLE 1: Analyze Single Repository from GitHub
────────────────────────────────────────────────────
  $ python3 enhanced_feature_evolution_analyzer.py
  
  Select input mode:
  1. GitHub Repository URL(s)
  2. Local Repository Path(s)
  3. CSV File with Metadata
  
  Enter your choice (1/2/3): 1
  
  Enter GitHub repository URL(s):
  👉 Enter URL(s): behave/behave
  
  ✅ Result:
     • Repository cloned
     • 8,310 commits analyzed
     • Feature evolution tracked
     • Reports generated in analysis_behave_*/ folder


EXAMPLE 2: Analyze Multiple Local Repositories
───────────────────────────────────────────────
  $ python3 enhanced_feature_evolution_analyzer.py
  
  Enter your choice (1/2/3): 2
  
  Enter local repository path(s):
  👉 Enter path(s): ./repos/project1, ./repos/project2, ./repos/project3
  
  ✅ Result:
     • Uses existing git history (FAST!)
     • 3 repositories analyzed
     • Parallel processing if available
     • All results in session folder


EXAMPLE 3: Batch Analysis from CSV
──────────────────────────────────
  Create repositories.csv:
  
  url,project_type,team
  cucumber/gherkin,Parser,Core
  cucumber/cucumber-ruby,Implementation,Core
  behave/behave,Framework,Community
  
  $ python3 enhanced_feature_evolution_analyzer.py
  
  Enter your choice (1/2/3): 3
  
  Enter CSV file path:
  👉 Enter CSV file path: repositories.csv
  
  ✅ Result:
     • All 3 repos analyzed
     • Metadata preserved
     • Comparative analysis possible
     • Session summary with all metrics


🔍 LOGGING & DEBUGGING
═══════════════════════════════════════════════════════════════════════════

View logs in real-time:
  $ tail -f evolution_analysis_results/session_*/evolution_analysis_*.log

Check specific errors:
  $ grep ERROR evolution_analysis_results/session_*/evolution_analysis_*.log

Debug specific repository:
  $ grep "behave" evolution_analysis_results/session_*/evolution_analysis_*.log


⏱️  PROGRESS TRACKING
═══════════════════════════════════════════════════════════════════════════

You'll see unified progress bars for:

  ① Repository cloning (if GitHub mode):
     Cloning repository: ████▌     | 50% [00:15<00:15]

  ② Commit analysis:
     Analyzing commits: ██████████| 100% [02:30<00:00]

  ③ Report generation (automatic, fast)


📊 EXECUTION SUMMARY
═══════════════════════════════════════════════════════════════════════════

At completion, you'll see:

  ======================================================================
  📊 EXECUTION SUMMARY
  ======================================================================
  
  ✅ Session Directory: evolution_analysis_results/session_20260413_193045
  📋 Log File: evolution_analysis_results/session_20260413_193045/evolution_analysis_20260413_193045.log
  
  📈 Repositories Analyzed:
     • Total: 3
     • Successful: 3
     • Failed: 0
  
  📊 Success Rate: 100.0%
  
  ⏱️  Duration: 0:45:30
  
  Repository Details:
    ✅ gherkin: 3545 commits analyzed
    ✅ behave: 8310 commits analyzed
    ✅ cucumber-ruby: 4728 commits analyzed
  
  ======================================================================
  ✅ Analysis complete! Check log file for detailed information.
  ======================================================================


⚠️  ERROR HANDLING
═══════════════════════════════════════════════════════════════════════════

The analyzer handles:

  ✓ Network failures → Logs error, continues with next repo
  ✓ Invalid URLs → Skips with warning, continues
  ✓ Permission errors → Reports and continues
  ✓ Large repositories → Handles efficiently with depth cloning
  ✓ CSV read errors → Validates and reports specific issues
  ✓ Visualization failures → Generates reports anyway
  ✓ Out of memory → Suitable for large commits due to streaming

All errors are logged with:
  • Timestamp
  • Error type
  • Root cause
  • Suggested fix


🎯 BEST PRACTICES
═══════════════════════════════════════════════════════════════════════════

1. Start small: Test with 1-2 repos first
   👉 Understand the output format

2. Use local paths for known repos: Much faster than cloning
   👉 2 hours to download vs 30 seconds to analyze local

3. Batch with CSV: Organize 10+ repositories efficiently
   👉 Single command vs multiple runs

4. Check logs for warnings: May have skipped some data
   👉 Read: evolution_analysis_results/session_*/evolution_analysis_*.log

5. Archive results: Keep session folders for comparison
   👉 evolution_analysis_results/session_20260413_193045/

6. Export data: Use CSV for further analysis
   👉 evolution_timeline.csv → Excel, R, Python pandas


🔗 INTEGRATION WITH BDD REPOSITORY CLONER
═══════════════════════════════════════════════════════════════════════════

Step 1: Clone all BDD repositories
  $ cd ../seart-tool-1-cloned-repos
  $ python3 clone_bdd_repos_seart_tool-1.py
  
  Enter CSV file name: seart-search-repos-consolidated-removed-duplicates-sorted-output.csv
  Enter folder name for cloned repositories: bdd_repos_analysis

Step 2: Analyze all cloned repositories
  $ cd ../feature-evolution-analyzer
  $ python3 enhanced_feature_evolution_analyzer.py
  
  Enter your choice (1/2/3): 2
  Enter path(s): ../seart-tool-1-cloned-repos/bdd_repos_analysis

Step 3: Get comprehensive BDD ecosystem insights
  ✅ Evolution analysis for 50+ BDD projects
  ✅ Compare development patterns
  ✅ Identify best practices
  ✅ Track test coverage growth


📞 SUPPORT & TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════

Issue: "Repository not found"
  → Verify URL: https://github.com/owner/repo
  → Check public access: Try in browser
  → Verify network: ping github.com

Issue: "Not a git repository"  
  → Ensure path has .git directory
  → Use: ls -la /path/to/repo | grep git

Issue: CSV column not found
  → CSV must have 'url' column
  → Check CSV header: head -1 file.csv

Issue: Memory issues with large repos
  → Analyze one per session
  → Use local mode (already cloned)
  → Increase system swap space

═══════════════════════════════════════════════════════════════════════════
Ready to analyze? Run: python3 enhanced_feature_evolution_analyzer.py
═══════════════════════════════════════════════════════════════════════════
""")
