# Beautiful Soup Web Scraping Process

## Overview

Beautiful Soup was used to **web scrape GitHub repositories for Gherkin BDD feature files**. The scraper navigated GitHub's web interface, parsed HTML, extracted links, and downloaded feature files for dataset creation.

---

## Input

**What we wanted to scrape:**
- GitHub repositories containing Gherkin BDD feature files (.feature files)
- Example: `https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master`

**Repository Features to Extract:**
- All `.feature` files (test scenario definitions in Gherkin language)
- Complete directory structure
- File metadata (size, line count, file path)

**Input Parameters:**
```python
repo_url = "https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master"
output_dir = "scraped_features"  # Where to save outputs
workers = 8  # Parallel processing threads
```

---

## Process

### Phase 1: URL Parsing & Validation

**Extract Repository Metadata:**
```python
URL: https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master

Extracted:
- owner: "naveenanimation20"
- repo: "CucumberSeleniumFramework"
- branch: "master"
```

**Branch Detection:**
- First, query GitHub API for default branch: `https://api.github.com/repos/{owner}/{repo}`
- If branch not found, try common candidates: `["main", "master", "develop", "dev", "trunk"]`
- Validate via GitHub API: `https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}`

### Phase 2: Directory Discovery (Hybrid Approach)

Beautiful Soup was used as a **fallback method** alongside GitHub API. The process:

**Method 1: GitHub API (Primary - Most Complete)**
```
Query: https://api.github.com/repos/owner/repo/git/trees/branch?recursive=1
Result: Complete tree structure with all directories and files
```

**Method 2: Beautiful Soup HTML Parsing (Fallback)**

When API failed or for supplementary discovery:

```python
def extract_file_paths_from_page(self, html: str) -> List[str]:
    """
    Parse GitHub HTML page and extract file/folder links.
    Uses Beautiful Soup to parse GitHub's dynamic HTML structure.
    """
    soup = BeautifulSoup(html, "html.parser")  # Parse HTML
    
    # Method 1: Look for GitHub's role="row" structure (current UI)
    for row in soup.find_all("div", {"role": "row"}):
        link_elem = row.find("a", href=True)
        if not link_elem:
            continue
        
        href = link.elem["href"]
        name = link_elem.get_text(strip=True)
        
        # Extract .feature files: GitHub uses /blob/ for files
        # Example: /owner/repo/blob/branch/path/to/file.feature
        if name.endswith(".feature") and "/blob/" in href:
            file_path = extract_path_from(href)  # → "path/to/file.feature"
            file_links.append(("file", file_path))
        
        # Extract directories: GitHub uses /tree/ for folders
        # Example: /owner/repo/tree/branch/path/to/folder
        if "/tree/" in href:
            folder_path = extract_path_from(href)  # → "path/to/folder"
            file_links.append(("dir", folder_path))
    
    # Method 2: Fallback regex-based extraction for edge cases
    if not file_links:
        for link in soup.find_all("a", href=True):
            # Parse any remaining feature files or directories
```

**Beautiful Soup Tasks:**
1. Parse HTML into DOM (soup object)
2. Find all `<div role="row">` elements (GitHub's file/folder rows)
3. Extract `<a>` tags containing links
4. Parse href attributes to identify files vs. folders
5. Extract file paths from GitHub URL structure

### Phase 3: Recursive Directory Traversal

```
Root Level:
├── pages scraped: 1
├── items found: ~20 files/folders

Level 2:
├── for each folder discovered:
│   ├── fetch HTML of /path/to/folder
│   ├── parse with BeautifulSoup
│   ├── extract sub-files and sub-folders
│   ├── add to queue

Result: Complete tree traversal discovering nested .feature files
```

### Phase 4: Feature File Content Download

For each `.feature` file discovered:

```
1. Construct raw content URL:
   https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}

2. Download file content (binary)

3. Validation: Check if file is English
   - Scan for Gherkin keywords: "feature:", "scenario:", "given", "when", "then"
   - Detect non-English Unicode patterns (Russian, Chinese, Arabic, etc.)
   - Require: At least 70% ASCII characters
   - Reject non-English files

4. Validation: Check if file has valid Gherkin structure
   - Must contain "given", "when", "then" keywords
   - Ensures only valid test scenarios are saved

5. Save to local directory preserving structure:
   scraped_features/
   └── {original_path_structure}
       └── file.feature
```

### Phase 5: Parallel Processing

**Concurrency Model:**
```python
ThreadPoolExecutor(max_workers=8)  # 8 parallel threads

Task Queue:
├── Thread 1: scrape folder1/
├── Thread 2: scrape folder2/
├── Thread 3: fetch file1.feature
├── Thread 4: fetch file2.feature
├── ... continue with 8 threads
```

**Benefits:**
- Faster scraping (I/O bound operations)
- Handles multiple HTTP requests simultaneously
- Progress tracking with TQDM

### Phase 6: Deduplication & Statistics

```python
visited_urls = set()  # Track visited pages to avoid re-scraping
found_items = {}     # Deduplicate file paths

Statistics Collected:
- total_feature_files: Count of .feature files
- total_lines: Sum of all line counts
- total_size_bytes: Total size of all files
- skipped_non_english: Count of rejected non-English files
```

---

## Output

### Output Structure

```
scraped_features/
├── manifest.json          ← Metadata file
├── examples/              ← Source code structure preserved
│   └── i18n/
│       └── en/
│           └── features/
│               └── addition.feature
├── features/
│   └── docs/
│       ├── exception_in_after_hook.feature
│       ├── exception_in_after_step_hook.feature
│       └── writing_support_code/
│           ├── attachments.feature
│           ├── load_path.feature
│           └── parameter_types.feature
└── issue.features/
    └── ...
```

### Output File 1: manifest.json

**Purpose:** Metadata summary of all scraped files

```json
{
  "repository": "behave/behave",
  "branch": "main",
  "output_dir": "scraped_features",
  "total_feature_files": 276,
  "total_lines": 34398,
  "total_size_bytes": 1163196,
  "feature_files": [
    {
      "path": "examples/i18n/en/features/addition.feature",
      "local_path": "scraped_features/examples/i18n/en/features/addition.feature",
      "size": 543,
      "lines": 17
    },
    {
      "path": "features/docs/exception_in_after_hook.feature",
      "local_path": "scraped_features/features/docs/exception_in_after_hook.feature",
      "size": 3630,
      "lines": 124
    }
  ]
}
```

### Output File 2: .feature files

**Example:** scraped_features/features/capture_stdout.feature

```gherkin
Feature: Capture stdout/stderr from Step Implementations
  Using a capture of stdout/stderr is often used to:
  
  * Verify that the step implementation produces expected output
  * To debug step implementations
  
  Current status: Just on Windows a little bit problematic
  (because of: different spawn behaviors)

  Scenario: Capture stdout in a step
    Given I have an active step
    When I call print("Hello World")
    Then captured stdout contains "Hello World"
  
  Scenario: Capture stderr in a step
    Given I have an active step
    When I call sys.stderr.write("Error Message")
    Then captured stderr contains "Error Message"
```

### Output Statistics (Actual Results)

**From behave/behave repository:**
```
✓ Feature Files Downloaded: 276
✓ Total Lines: 34,398
✓ Total Size: 1,163,196 bytes (~1.1 MB)
✓ Coverage: Multiple feature directories
✓ Languages: English (filtered for language)
✓ Quality: All files validated for Gherkin structure
```

**Across Multiple Repositories:**
```
Repository: naveenanimation20/CucumberSeleniumFramework
├── Files: 15+
├── Total Lines: 1,250+
├── Size: 45 KB+
└── Status: ✓ Append mode working

Repository: behave/behave
├── Files: 276
├── Total Lines: 34,398
├── Size: 1.1 MB
└── Status: ✓ Successfully scraped

Total Dataset:
├── Repositories: 2+
├── Feature Files: 290+
├── Total Lines: 35,000+
└── Size: 1.1+ MB
```

---

## Key Beautiful Soup Operations

### 1. Parse HTML
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
```

### 2. Find File/Folder Rows
```python
# GitHub's file listing uses role="row" divs
for row in soup.find_all("div", {"role": "row"}):
    link = row.find("a", href=True)
```

### 3. Extract Links
```python
href = link["href"]           # Get URL
name = link.get_text(strip=True)  # Get display text
```

### 4. Parse GitHub URLs
```python
# File: /blob/ structure
if "/blob/" in href:
    file_path = href.split("/blob/branch/", 1)[1]

# Folder: /tree/ structure
if "/tree/" in href:
    folder_path = href.split("/tree/branch/", 1)[1]
```

### 5. Fallback HTML Parsing
```python
# If structured parsing fails, fall back to regex-based scanning
for link in soup.find_all("a", href=True):
    if ".feature" in href and "/blob/" in href:
        # Extract and validate
```

---

## Evolution: Why Beautiful Soup + API Hybrid Approach

### Initial Problem
- **Original approach**: HTML-only with Beautiful Soup
- **Issue**: GitHub's JavaScript rendering meant some content wasn't in the HTML
- **Result**: 0 files found for complex nested structures

### Solution Implemented
1. **Primary method**: GitHub API (`git/trees?recursive=1`)
   - Complete tree traversal
   - No missing nested directories
   - More reliable

2. **Fallback method**: Beautiful Soup HTML parsing
   - Catches edge cases API misses
   - Handles rate limiting gracefully
   - Works as backup when API unavailable

### Current Status
- **Hybrid approach**: API + Beautiful Soup for maximum coverage
- **Success rate**: Near-perfect directory discovery
- **Robustness**: Handles rate limiting, redirects, and edge cases

---

## Beautiful Soup Value in This Project

| Aspect | Role |
|--------|------|
| **HTML Parsing** | Parse GitHub's HTML page structure |
| **DOM Navigation** | Find links nested in complex HTML |
| **Link Extraction** | Identify .feature files and directories |
| **Fallback Discovery** | Catch items missed by other methods |
| **Language Support** | Works with any HTML parser backend |
| **Robustness** | Graceful handling of malformed HTML |

---

## Comparison: Beautiful Soup vs. GitHub API

| Factor | Beautiful Soup | GitHub API |
|--------|---|---|
| **Coverage** | Partial (visible items) | Complete (with recursive) |
| **Rate Limits** | High (~60 req/min) | Lower (~60 req/min with auth) |
| **Speed** | Slower (parsing HTML) | Faster (JSON) |
| **Edge Cases** | Can miss nested dirs | Comprehensive |
| **Fallback** | N/A | Yes (to Beautiful Soup) |
| **Role** | Fallback/supplement | Primary |

---

## Summary: Input → Process → Output

```
INPUT:
  GitHub URL → Repository metadata (owner, repo, branch)
  
PROCESS:
  1. Branch detection (API-first)
  2. Directory discovery (API + Beautiful Soup parsing)
  3. Beautiful Soup extracts links from GitHub HTML:
     - Parse role="row" divs
     - Find <a> tags with href
     - Identify /blob/ (files) vs /tree/ (folders)
  4. Recursive traversal of folders
  5. Download and validate .feature files
  6. Parallel processing (8 threads)
  7. Deduplication & statistics
  
OUTPUT:
  ✓ 276+ feature files scraped
  ✓ 34,000+ lines preserved
  ✓ Directory structure maintained
  ✓ manifest.json with metadata
  ✓ Language validation (English-only)
  ✓ Gherkin structure validation
```

---

## Related to Research

**Connection to RAGAS Evaluation:**
- Scraped real feature files from OSS projects
- Created dataset of authentic BDD test scenarios
- This dataset could be used to create ground truth for RAGAS evaluation
- Current RAGAS evaluation uses synthetic scenarios instead of mined ones
- Future work: Integrate scraped features into evaluation framework

**Connection to PyDriller Mining:**
- Beautiful Soup scraped from GitHub web interface
- PyDriller mined from Git commit history (deeper analysis)
- Both approaches discover Gherkin content but from different angles
- Beautiful Soup: Fast web-based discovery
- PyDriller: Historical analysis, evolution tracking, commit details

