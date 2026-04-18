#!/bin/bash
# Quick usage guide for GitHub Feature File Scrapers

echo "=========================================="
echo "GitHub Feature File Scraper - Quick Start"
echo "=========================================="
echo ""

REPO_URL="https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master"
OUTPUT_DIR="scraped_features"

echo "Repository: $REPO_URL"
echo "Output Directory: $OUTPUT_DIR"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 not found. Please install Python 3."
    exit 1
fi

# Check dependencies
echo "Checking dependencies..."
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing requests..."
    pip install requests
fi

python3 -c "import bs4" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing beautifulsoup4 (optional, for web scraper)..."
    pip install beautifulsoup4
fi

echo ""
echo "Dependencies installed ✓"
echo ""

# Option 1: API-based (recommended)
echo "=== Option 1: API-Based Scraper (RECOMMENDED) ==="
echo "This is faster and more reliable."
echo ""
echo "Command:"
echo "  python3 github_feature_scraper_api.py \"$REPO_URL\""
echo ""
echo "With GitHub token (recommended for higher rate limits):"
echo "  export GITHUB_TOKEN=your_token"
echo "  python3 github_feature_scraper_api.py \"$REPO_URL\""
echo ""

# Option 2: Web scraper
echo "=== Option 2: Web Scraper (BeautifulSoup) ==="
echo "This uses web scraping."
echo ""
echo "Command:"
echo "  python3 github_feature_scraper.py \"$REPO_URL\""
echo ""

echo "=========================================="
echo "To start scraping, run one of these:"
echo ""
echo "API-based (fast, recommended):"
echo "  python3 github_feature_scraper_api.py '$REPO_URL'"
echo ""
echo "Web scraper (slower, uses BeautifulSoup):"
echo "  python3 github_feature_scraper.py '$REPO_URL'"
echo ""
echo "=========================================="
