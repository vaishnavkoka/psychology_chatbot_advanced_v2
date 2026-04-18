# GitHub Feature File Scraper - Usage Examples

## Flexible URL Formats

The scraper now accepts multiple URL formats:

### 1. Simple Format (owner/repo)
```bash
python3 github_feature_scraper.py "naveenanimation20/CucumberSeleniumFramework"
```

### 2. Full HTTPS URL
```bash
python3 github_feature_scraper.py "https://github.com/naveenanimation20/CucumberSeleniumFramework"
```

### 3. With Explicit Branch
```bash
python3 github_feature_scraper.py "https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master"
```

### 4. With File Path (uses repo root automatically)
```bash
python3 github_feature_scraper.py "https://github.com/cucumber/cucumber/blob/master/features/step_definitions.rb"
```

**Key Point:** All formats automatically search the ENTIRE REPOSITORY for .feature files, starting from the repository root.

---

## Parallel Performance

```bash
# Fast: 6-8 workers (default is 4)
python3 github_feature_scraper.py "naveenanimation20/CucumberSeleniumFramework" --workers 8

# Moderate load: 4 workers
python3 github_feature_scraper.py "naveenanimation20/CucumberSeleniumFramework" --workers 4

# Slow: 1 worker (safest for rate limits)
python3 github_feature_scraper.py "naveenanimation20/CucumberSeleniumFramework" --workers 1
```

---

## Accumulate Features from Multiple Repos

The `--append` flag allows you to build a combined dataset from multiple repositories.

### Without Append (default - replaces old files)
```bash
python3 github_feature_scraper.py "repo1/owner1"              # scraped_features/ has 50 files
python3 github_feature_scraper.py "repo2/owner2"              # scraped_features/ has 30 files (previous replaced)
```

### With Append (keeps all files)
```bash
python3 github_feature_scraper.py "repo1/owner1"              # scraped_features/ has 50 files
python3 github_feature_scraper.py "repo2/owner2" --append     # scraped_features/ has 80 files (50+30)
python3 github_feature_scraper.py "repo3/owner3" --append     # scraped_features/ has 120 files (50+30+40)
```

#### Example Workflow:
```bash
# Create dataset from multiple BDD test repositories
python3 github_feature_scraper.py "naveenanimation20/CucumberSeleniumFramework"
python3 github_feature_scraper.py "gherkin-lint/gherkin-lint" --append
python3 github_feature_scraper.py "cucumber/cucumber-js" --append
python3 github_feature_scraper.py "behave/behave" --append

# Now scraped_features/manifest.json contains all .feature files from all repos!
cat scraped_features/manifest.json | grep total_feature_files
```

---

## Debugging & Verbose Mode

### Verbose Mode - See What's Happening
```bash
python3 github_feature_scraper.py "gherkin-lint/gherkin-lint" --verbose
```

Output shows:
- Branch detection attempts
- Which branches were tested
- Directory traversal progress
- Error details

### Help
```bash
python3 github_feature_scraper.py --help
```

---

## Complete Example - Build LLM Training Dataset

```bash
#!/bin/bash
# Scrape multiple BDD repositories into one dataset

OUTPUT_DIR="my_gherkin_dataset"

echo "Starting Gherkin Feature Mining..."

# First repo (clears directory)
python3 github_feature_scraper.py "cucumber/cucumber" \
    --output-dir "$OUTPUT_DIR" \
    --workers 6

# Additional repos (append to dataset)
for repo in \
    "behave/behave" \
    "gherkin-lint/gherkin-lint" \ "naveenanimation20/CucumberSeleniumFramework" \
    "cucumber/cucumber-js" \
    "jbehave/jbehave"
do
    echo "Adding $repo..."
    python3 github_feature_scraper.py "$repo" \
        --output-dir "$OUTPUT_DIR" \
        --workers 4 \
        --append
done

# Check final results
echo ""
echo "✅ Mining complete!"
echo "Total features: $(find $OUTPUT_DIR -name "*.feature" | wc -l)"
echo "Summary: $(cat $OUTPUT_DIR/manifest.json | grep total_feature_files)"
```

---

## Output Structure

```
scraped_features/
├── manifest.json                    # Metadata about all scraped files
├── test/
│   ├── linter/
│   │   ├── MultilineStep.feature
│   │   ├── NoViolations.feature
│   │   └── ...
│   └── rules/
│       ├── no-partially-commented-tag-lines/
│       │   ├── NoViolations.feature
│       │   └── Violations.feature
│       └── ...
├── src/
│   └── main/
│       └── java/
│           └── Features/
│               ├── contacts.feature
│               ├── deals.feature
│               └── ...
└── ... (all other folders with .feature files)
```

### Manifest Structure
```json
{
  "repository": "gherkin-lint/gherkin-lint",
  "branch": "master",
  "output_dir": "scraped_features",
  "total_feature_files": 110,
  "total_lines": 3245,
  "total_size_bytes": 89234,
  "feature_files": [
    {
      "path": "test/linter/MultilineStep.feature",
      "local_path": "scraped_features/test/linter/MultilineStep.feature",
      "size": 890,
      "lines": 23
    },
    ...
  ],
  "errors": []
}
```

---

## Complete Example - LLM Training

```bash
# Build training dataset from 10 popular BDD repositories
python3 github_feature_scraper.py "cucumber/cucumber"
python3 github_feature_scraper.py "behave/behave" --append --workers 6
python3 github_feature_scraper.py "gherkin-lint/gherkin-lint" --append --workers 6
# ... add more repos with --append

# Now use the files for LLM training
python3 << 'PYTHON'
import json
from pathlib import Path

# Load manifest
with open('scraped_features/manifest.json') as f:
    manifest = json.load(f)

print(f"Training dataset ready!")
print(f"Total features: {manifest['total_feature_files']}")
print(f"Total lines of Gherkin: {manifest['total_lines']}")
print(f"Total size: {manifest['total_size_bytes'] / 1024 / 1024:.2f} MB")

# Use for training...
for feature in manifest['feature_files']:
    file_path = Path(feature['local_path'])
    # Read and process for LLM training
PYTHON
```

