#!/usr/bin/env python3
"""
SIMPLE USAGE GUIDE - PyDriller BDD Mining Tool

This tool is designed for simplicity:
1. Run the program
2. Enter a GitHub URL
3. Get CSV results

That's it!
"""

# ============================================================================
# QUICK START
# ============================================================================

"""
1. Navigate to the folder:
   cd /home/vaishnavkoka/RE4BDD/Mining/pydriller-mining

2. Run the tool:
   python pydriller_quickstart.py

3. Follow the prompts and mining starts automatically!
"""

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
Example 1: Mine Cucumber JavaScript
───────────────────────────────────

$ python pydriller_quickstart.py

📍 Enter GitHub repository URL: https://github.com/cucumber/cucumber-js
📝 Repository name [cucumber-js]: 
🌿 Branch name [main]: 

(Automated extraction and CSV export)

✅ Done!


Example 2: Mine Behave Framework
─────────────────────────────────

$ python pydriller_quickstart.py

📍 Enter GitHub repository URL: https://github.com/behave/behave
📝 Repository name [behave]:
🌿 Branch name [master]:

(Automated extraction and CSV export)

✅ Done!


Example 3: Mine Multiple Repos
──────────────────────────────

$ python pydriller_quickstart.py

📍 Enter GitHub repository URL: https://github.com/cucumber/cucumber-js
📝 Repository name [cucumber-js]: 
🌿 Branch name [main]: 

✅ Mining Complete!

⚡ Mine another repository? (yes/no): yes

📍 Enter GitHub repository URL: https://github.com/behave/behave
📝 Repository name [behave]: 
🌿 Branch name [master]: 

✅ Mining Complete!

⚡ Mine another repository? (yes/no): no

👋 Thank you for using PyDriller BDD Mining!
"""

# ============================================================================
# OUTPUT FILES
# ============================================================================

"""
After mining, you'll find CSV files in:
../mining_outputs/

Example outputs:
  • cucumber-js_features.csv          (Feature data)
  • cucumber-js_repositories.json     (Full repo details)
  • cucumber-js_summary.txt           (Human-readable report)
"""

# ============================================================================
# CSV COLUMNS
# ============================================================================

"""
The CSV file contains:

Column              | Example
────────────────────┼──────────────────────────────
repo_name           | cucumber-js
feature_file        | features/cli.feature
scenario_count      | 8
scenarios           | Login | Logout | Help Command
commits             | 23
first_seen          | 2023-01-15T10:20:30.123456
last_modified       | 2024-03-10T14:55:20.456789
"""

# ============================================================================
# PYTHON CODE EXAMPLE
# ============================================================================

"""
To use in Python directly (instead of interactive CLI):

from pydriller_feature_miner import PyDrillerFeatureMiner

miner = PyDrillerFeatureMiner(output_prefix="my-repo")
miner.mine_repository(
    repo_url="https://github.com/cucumber/cucumber-js",
    repo_name="Cucumber JS",
    branch="main"
)
miner._export_results()

# Results saved to CSV!
"""

# ============================================================================
# SUPPORTED REPOSITORIES
# ============================================================================

"""
Popular BDD repositories to mine:

1. Cucumber JavaScript
   https://github.com/cucumber/cucumber-js

2. Cucumber Python
   https://github.com/cucumber/cucumber-python

3. Behave (Python BDD Framework)
   https://github.com/behave/behave

4. pytest-BDD
   https://github.com/pytest-dev/pytest-bdd

5. Dredd (API Testing)
   https://github.com/apiaryio/dredd

6. Cucumber JVM (Java)
   https://github.com/cucumber/cucumber-jvm
"""

# ============================================================================
# REQUIREMENTS
# ============================================================================

"""
Before running:

pip install -r pydriller_requirements.txt

This installs:
- pydriller (Git mining)
- pandas (Data processing)
- requests (HTTP)
- gitpython (Git utilities)
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Q: Program won't start?
A: Make sure dependencies are installed:
   pip install -r pydriller_requirements.txt

Q: Invalid URL error?
A: Use full GitHub HTTPS URL:
   ✅ https://github.com/owner/repo
   ❌ github.com/owner/repo
   ❌ https://git@github.com:owner/repo

Q: Repository not found?
A: Check:
   1. URL is correct
   2. Repository is public
   3. Branch exists (default: main)

Q: No scenarios found?
A: Repository might not have .feature files, or they're not 
   in the standard locations (features/, etc.)

Q: Where are the CSV files?
A: Look in: ../mining_outputs/
   Or: /home/vaishnavkoka/RE4BDD/Mining/mining_outputs/
"""

# ============================================================================
# NEXT STEPS
# ============================================================================

"""
After mining, you can:

1. Load CSV in Pandas:
   import pandas as pd
   df = pd.read_csv("../mining_outputs/cucumber-js_features.csv")
   print(df)

2. Use in RAGAS evaluation:
   See: ../Ragas/ragas_eval_requirements.ipynb

3. Combine multiple CSVs:
   df1 = pd.read_csv("cucumber-js_features.csv")
   df2 = pd.read_csv("behave_features.csv")
   combined = pd.concat([df1, df2])

4. Create visualizations:
   df.plot()
   df['scenario_count'].hist()
   df.groupby('repo_name').sum()
"""

# ============================================================================
# THAT'S IT!
# ============================================================================

"""
Your PyDriller mining tool is ready! 🚀

Simply run:
  python pydriller_quickstart.py

And start mining GitHub repos!
"""
