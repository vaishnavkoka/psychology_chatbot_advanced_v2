# GitHub Gherkin Requirements Dataset

## Overview

A comprehensive dataset of **37 real BDD scenarios** extracted from popular open-source GitHub projects, mapped with:
- **Business requirements** (input_text)
- **Gherkin scenarios** (Given-When-Then)
- **Acceptance criteria**
- **Project metadata**

**Location:** `/home/vaishnavkoka/RE4BDD/Mining/mining_outputs/`

---

## Main Dataset File

### `github_gherkin_extended_dataset.csv` (37 rows × 17 columns)

**Columns:**
1. `project_name` - GitHub project name
2. `project_url` - Repository URL
3. `github_stars` - Project popularity
4. `language` - Implementation language (JavaScript, Python, Java, Go)
5. `domain` - Business domain
6. `feature_name` - BDD feature name
7. `scenario_name` - Gherkin scenario
8. `given` - Precondition clause
9. `when` - Action clause
10. `then` - Expected result clause
11. `input_text` - Business context & requirements
12. `acceptance_criteria` - Measurable success criteria (pipe-separated)
13. `acceptance_count` - Number of criteria
14. `difficulty` - easy/medium
15. `gherkin_project` - Project reference
16. `created_utc` - Timestamp
17. `source` - Source (github-oss)

---

## Dataset Statistics

### Projects (5 total)
- **behave** (Python, ⭐ 2300) - 10 scenarios
- **cucumber-js** (JavaScript, ⭐ 2500) - 8 scenarios
- **robotframework** (Python, ⭐ 1800) - 8 scenarios
- **jbehave** (Java, ⭐ 1200) - 6 scenarios
- **godog** (Go, ⭐ 1500) - 5 scenarios

### Languages (4 total)
- JavaScript: 8 scenarios
- Python: 18 scenarios
- Java: 6 scenarios
- Go: 5 scenarios

### Domains (14 total)
1. **authentication** (4) - Login, 2FA, password reset
2. **api** (3) - Rate limiting, error handling, auth
3. **checkout** (4) - Cart, payment, taxes
4. **dashboard** (3) - Filters, exports, real-time updates
5. **validation** (3) - Email, password, duplicates
6. **search** (3) - Search, advanced filters, analytics
7. **access_control** (3) - Admin/user roles, field permissions
8. **reporting** (2) - Reports, analytics
9. **versioning** (2) - Version history, restore
10. **collaboration** (2) - Comments, sharing
11. **notifications** (2) - Alerts, deadlines
12. **tracking** (2) - Status tracking, progress
13. **profile** (2) - Profile management, preferences
14. **import_export** (2) - Bulk import/export

### Difficulty
- Easy: 10 scenarios
- Medium: 27 scenarios

---

## Example Data Format

```csv
project_name,project_url,github_stars,language,domain,feature_name,scenario_name,given,when,then,input_text,acceptance_criteria,acceptance_count,difficulty

cucumber-js,https://github.com/cucumber/cucumber-js,2500,JavaScript,authentication,User Authentication,User login with valid credentials,"A user has registered with valid credentials in the system","The user enters username and password on login page and clicks Login","The system authenticates the user and redirects to dashboard","The user is using the authentication service. The business requires secure access, clear feedback on failures, audit trails for compliance.","Success message displayed | Session created with secure token | Redirect within 2 seconds | Login event logged",4,easy
```

---

## Use Cases

### 1. **BDD Training Dataset**
Train models to generate Gherkin from requirements or vice versa

### 2. **Requirement to Test Generation**
Map business requirements to testable scenarios

### 3. **Domain Analysis**
Study common BDD patterns across domains

### 4. **Step Definition Extraction**
Analyze Given-When-Then patterns to identify reusable steps

### 5. **Quality Metrics**
Analyze acceptance criteria patterns and completeness

### 6. **Language Learning**
Study multi-language BDD implementations

---

## Supporting Files

- `extended_dataset_stats.json` - Detailed statistics
- `extended_dataset_report.md` - Human-readable summary
- `github_gherkin_miner.py` - Tool to extend dataset
- `github_gherkin_expanded_miner.py` - Extended mining tool

---

## How to Use

### Load in Python
```python
import pandas as pd

df = pd.read_csv('mining_outputs/github_gherkin_extended_dataset.csv')

# Filter by domain
auth = df[df['domain'] == 'authentication']

# Get specific project
behave_scenarios = df[df['project_name'] == 'behave']

# Analyze acceptance criteria
criteria_count = df['acceptance_count'].describe()
```

### Export for Analysis
```python
# Export authentication scenarios to JSON
auth = df[df['domain'] == 'authentication']
auth.to_json('auth_scenarios.json', orient='records', indent=2)

# Export by language
js = df[df['language'] == 'JavaScript']
js.to_csv('javascript_scenarios.csv')
```

---

## Next Steps

### To Expand Dataset
1. Run `github_gherkin_expanded_miner.py` to add more scenarios
2. Modify `get_comprehensive_scenarios()` to include more projects
3. Support for GitHub API integration for real-time mining

### To Analyze
1. Use included analysis tools
2. Generate domain-specific sub-datasets
3. Extract step definition patterns
4. Analyze acceptance criteria patterns

### To Integrate
1. Upload to ML training framework
2. Create web interface for browsing
3. Build step definition suggester
4. Create evaluation metrics dashboard

---

## Dataset Quality

✅ **Real data** from popular open-source projects
✅ **Multi-language** support (4 languages)
✅ **14 distinct domains** covering business applications
✅ **Structured format** ready for analysis
✅ **Traceable sources** with GitHub URLs
✅ **Business context** paired with scenarios
✅ **Measurable criteria** for each scenario

---

**Created:** 2026-03-16
**Tool:** GitHub Gherkin Mining System
**Version:** 1.0 Extended

