# GitHub Feature File Scraper

Two Python scripts to scrape all `.feature` files from a GitHub repository.

## Quick Start

### Option 1: API-Based Scraper (RECOMMENDED) ⭐

Faster, more reliable, uses GitHub API:

```bash
# Optional: Use your GitHub token for higher rate limits
export GITHUB_TOKEN=your_token

# Run the scraper
python3 github_feature_scraper_api.py https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master

# Output will be saved in scraped_features/ directory
```

### Option 2: Web Scraper (BeautifulSoup)

Uses web scraping with BeautifulSoup:

```bash
python3 github_feature_scraper.py https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master

# Output will be saved in scraped_features/ directory
```

## Files

- `github_feature_scraper.py` - BeautifulSoup-based web scraper
- `github_feature_scraper_api.py` - GitHub API-based scraper (recommended)

## Usage

### API-Based Scraper (Recommended)

```bash
export GITHUB_TOKEN=your_token
python3 github_feature_scraper_api.py <REPO_URL> [--output-dir DIR]
```

**Arguments:**
- `REPO_URL` - GitHub repository URL (e.g., `https://github.com/owner/repo/tree/branch`)
- `--output-dir` - Output directory (default: `scraped_features`)

**Example:**
```bash
python3 github_feature_scraper_api.py https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master --output-dir my_features
```

### Web Scraper (BeautifulSoup)

```bash
python3 github_feature_scraper.py <REPO_URL> [--output-dir DIR]
```

**Arguments:**
- `REPO_URL` - GitHub repository URL
- `--output-dir` - Output directory (default: `scraped_features`)

## Output

Both scrapers create:

1. **Directory structure** - Local copy of .feature files with original folder structure
2. **manifest.json** - Summary of all scraped files:
   - Total feature files count
   - Total lines of code
   - Total size in bytes
   - List of all feature files with their paths
   - Any errors encountered

### Example Output Structure

```
scraped_features/
├── manifest.json
├── src/
│   └── test/
│       └── feature/
│           ├── login.feature
│           ├── checkout.feature
│           └── cart/
│               └── add_item.feature
```

### Example manifest.json

```json
{
  "repository": "naveenanimation20/CucumberSeleniumFramework",
  "branch": "master",
  "output_dir": "scraped_features",
  "total_feature_files": 15,
  "total_lines": 1250,
  "total_size_bytes": 45000,
  "feature_files": [
    {
      "path": "src/test/feature/login.feature",
      "local_path": "scraped_features/src/test/feature/login.feature",
      "size": 3000,
      "lines": 45
    }
  ],
  "errors": []
}
```

## Comparison

| Feature | Web Scraper | API Scraper |
|---------|-------------|------------|
| Speed | Slower | **Faster** ✓ |
| Rate Limit | 60 req/hr | 5000 req/hr (with token) |
| Reliability | Fragile (HTML changes) | **Robust** ✓ |
| Dependencies | BeautifulSoup | requests |
| Recommended | ❌ | ✅ |

## Installation

```bash
# Install required packages
pip install requests beautifulsoup4

# Or for specific scrapers:

# API scraper only
pip install requests

# Web scraper only
pip install beautifulsoup4 requests
```

## Rate Limits

### Without GitHub Token
- 60 API requests per hour
- ~5-10 repositories before hitting limit

### With GitHub Token
- 5000 API requests per hour
- Recommended for production use

### Setting GitHub Token

```bash
# Create a token at https://github.com/settings/tokens
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Verify it's set
echo $GITHUB_TOKEN
```

## Error Handling

Both scrapers:
- Log errors to console
- Save errors to manifest.json
- Continue scraping despite errors
- Show summary of successes and failures

## Example Usage

### Scrape CucumberSeleniumFramework

```bash
export GITHUB_TOKEN=your_token
python3 github_feature_scraper_api.py https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master
```

### Scrape with Custom Output Directory

```bash
python3 github_feature_scraper_api.py https://github.com/user/repo/tree/main --output-dir ./features_dump
```

### Scrape Different Branch

```bash
python3 github_feature_scraper_api.py https://github.com/user/repo/tree/develop
```

## Troubleshooting

### "Rate limit reached"
- Set up GitHub token: `export GITHUB_TOKEN=your_token`
- Use API scraper instead of web scraper

### "Invalid GitHub URL"
- Use full repository URL with branch: `https://github.com/owner/repo/tree/branch`
- Don't use shortened URLs or trailing slashes

### "No feature files found"
- Verify the repository has .feature files
- Check the branch name is correct

### Permission Errors
- Ensure output directory is writable
- Use `--output-dir` to specify a different location

## Next Steps

After scraping, you can:
1. Use the feature files with your testing framework (Cucumber, Behave, etc.)
2. Analyze the features using natural language processing
3. Train ML models on the feature files
4. Integrate with CI/CD pipelines

## License

These scripts are provided as-is for educational and commercial use.
