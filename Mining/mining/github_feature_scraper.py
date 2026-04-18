"""
GitHub Feature File Web Scraper using BeautifulSoup

Scrapes all .feature files from a GitHub repository given its web URL.
Navigates through folder structure and downloads feature file contents.

Usage:
    python3 github_feature_scraper.py https://github.com/owner/repo/tree/branch
    
Example:
    python3 github_feature_scraper.py https://github.com/naveenanimation20/CucumberSeleniumFramework/tree/master
"""

import argparse
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class GitHubFeatureScraper:
    """Scrapes .feature files from GitHub repositories using BeautifulSoup."""

    # English language keywords commonly found in .feature files
    ENGLISH_KEYWORDS = {
        "feature:", "scenario:", "scenario outline:", "given ", "when ", "then ", "and ", "but ",
        "examples:", "background:", "rule:", "*", "@", "#"
    }
    
    # Non-English language markers (Russian, Chinese, Arabic, etc.)
    NON_ENGLISH_PATTERNS = [
        r'[\u0400-\u04FF]',  # Cyrillic (Russian, Bulgarian, etc.)
        r'[\u4E00-\u9FFF]',  # CJK Unified Ideographs (Chinese, Japanese)
        r'[\u3040-\u309F]',  # Hiragana (Japanese)
        r'[\u30A0-\u30FF]',  # Katakana (Japanese)
        r'[\u0600-\u06FF]',  # Arabic
        r'[\u0E00-\u0E7F]',  # Thai
        r'[\u0900-\u097F]',  # Devanagari (Hindi)
    ]

    def __init__(self, repo_url: str, output_dir: str = "scraped_features", workers: int = 8, verbose: bool = False, fresh: bool = False):
        """
        Initialize the scraper.

        Args:
            repo_url: GitHub repository URL (flexible formats supported)
            output_dir: Directory to save scraped feature files
            workers: Number of parallel workers for scraping (default: 8, use 1-16 for optimal performance)
            verbose: Enable verbose logging (default: False)
            fresh: Clear existing files before scraping (default: False - append instead)
        """
        self.repo_url = repo_url.rstrip("/")
        self.output_dir = Path(output_dir)
        self.fresh_mode = fresh
        
        # Clear directory only if --fresh flag is used
        if fresh:
            if self.output_dir.exists():
                import shutil
                shutil.rmtree(self.output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
            print(f"🗑️  Fresh start: Cleared old files\n")
        else:
            # Default: append mode - just create if doesn't exist
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.workers = max(1, min(workers, 16))  # Clamp to 1-16 range
        self.verbose = verbose
        self.english_only = True  # Filter non-English .feature files
        self.skipped_non_english = 0

        # Initialize session FIRST (before parse_repo_info)
        # Use connection pooling for better performance with many requests
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=max(self.workers * 2, 16),
            pool_maxsize=max(self.workers * 2, 16),
            max_retries=requests.adapters.Retry(
                total=2,
                backoff_factor=0.3,
                status_forcelist=(500, 502, 503, 504)
            )
        )
        self.session = requests.Session()
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

        # Parse repository info from URL
        self.parse_repo_info()

        self.visited_urls: Set[str] = set()
        self.feature_files: List[Dict[str, str]] = []
        self.errors: List[str] = []
        self.pbar_files = None
        self.pbar_dirs = None

    def parse_repo_info(self) -> None:
        """Extract owner, repo name, and branch from GitHub URL."""
        # Normalize URL - accept various formats
        url = self.repo_url.strip()
        
        # If it doesn't start with https, assume it's owner/repo format
        if not url.startswith("http"):
            url = f"https://github.com/{url}"
        
        # Remove trailing slashes
        url = url.rstrip("/")
        
        # Pattern: https://github.com/owner/repo[/tree/branch][/path/to/file]
        # Match owner/repo first, then optionally branch and path
        match = re.search(r"github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?(?:/.*)?$", url)

        if not match:
            raise ValueError(f"Invalid GitHub URL: {self.repo_url}")

        self.owner = match.group(1)
        self.repo = match.group(2)
        provided_branch = match.group(3)
        
        # If no branch provided, try to detect it automatically
        if provided_branch:
            self.branch = provided_branch
        else:
            if self.verbose:
                print("🔍 Detecting default branch...")
            detected_branch = self._detect_default_branch()
            if detected_branch:
                self.branch = detected_branch
                if self.verbose:
                    print(f"   ✓ Found default branch: {self.branch}")
            else:
                # Fallback to main
                self.branch = "main"
                if self.verbose:
                    print(f"   ⚠️  Branch detection failed, using fallback: {self.branch}")

        # Construct the raw content base URL for this repo
        self.raw_base_url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}"
        self.web_base_url = f"https://github.com/{self.owner}/{self.repo}/tree/{self.branch}"

        print(f"Repository: {self.owner}/{self.repo}")
        print(f"Branch: {self.branch}")
        if self.verbose:
            print(f"Web Base URL: {self.web_base_url}")
        print()

    def _detect_default_branch(self) -> Optional[str]:
        """Try to detect the repository's default branch using GitHub API."""
        # First, try to get the default branch from API (most reliable)
        try:
            api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
            resp = self.session.get(api_url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                default_branch = data.get("default_branch")
                if default_branch:
                    if self.verbose:
                        print(f"   Via API: {default_branch}")
                    return default_branch
        except Exception as e:
            if self.verbose:
                print(f"   API detection error: {e}")
        
        # Fallback: Try common branch names via API tree endpoint (more reliable than web URLs)
        candidates = ["main", "master", "develop", "dev", "trunk"]
        
        for branch in candidates:
            try:
                # Test via API which is more accurate than web redirects
                api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{branch}"
                resp = self.session.head(api_url, timeout=5)
                if resp.status_code == 200:
                    if self.verbose:
                        print(f"   Found branch via API: {branch}")
                    return branch
            except Exception as e:
                if self.verbose:
                    print(f"   Branch {branch} error: {e}")
                continue
        
        return None

    def get_all_directories_api(self, path: str = "", recursive: bool = True) -> List[str]:
        """
        Get all directories from a repository using GitHub API.
        This is more reliable than HTML scraping for complete tree traversal.
        """
        directories = []
        
        try:
            # Use GitHub API to get repository tree
            api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{self.branch}?recursive=1"
            
            if self.verbose:
                print(f"  🔗 Querying GitHub API: {api_url}")
            
            resp = self.session.get(api_url, timeout=10)
            
            if resp.status_code == 404:
                if self.verbose:
                    print(f"  ⚠️  Branch '{self.branch}' not found in GitHub API repository")
                    print(f"     (Note: Branch might exist on web but not in git tree)")
                return directories
            elif resp.status_code != 200:
                if self.verbose:
                    print(f"  ⚠️  API returned status {resp.status_code}, falling back to HTML parsing")
                return directories
            
            data = resp.json()
            
            # Extract all unique directories from the tree
            seen_dirs = set()
            for item in data.get("tree", []):
                if item["type"] == "tree":  # It's a directory
                    dir_path = item["path"]
                    # Add all parent directories
                    parts = dir_path.split("/")
                    for i in range(1, len(parts)):
                        parent = "/".join(parts[:i])
                        if parent not in seen_dirs:
                            directories.append(parent)
                            seen_dirs.add(parent)
            
            if self.verbose and directories:
                print(f"  ✓ Found {len(directories)} directories via API")
            elif self.verbose:
                print(f"  ℹ️  No directories found via API tree")
            
            return directories
        except Exception as e:
            if self.verbose:
                print(f"  ⚠️  API error: {e}")
            return directories

    def get_page_html(self, url: str) -> Optional[str]:
        """Fetch HTML content from a GitHub URL with retry logic."""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, timeout=10)
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code == 404:
                    # Not found - don't retry
                    return None
                elif resp.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = int(resp.headers.get('Retry-After', retry_delay))
                    print(f"  ⚠️  Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    retry_delay = wait_time * 2
                    continue
                else:
                    # Other error - retry with backoff
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    return None
            except Exception as exc:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                return None
        
        return None

    def is_english_feature_file(self, content: str) -> bool:
        """Check if a feature file is in English by analyzing its content."""
        if not content or len(content.strip()) < 10:
            return False
        
        content_lower = content.lower()
        
        # Check for non-English Unicode characters
        for pattern in self.NON_ENGLISH_PATTERNS:
            if re.search(pattern, content):
                return False
        
        # Check for English Gherkin keywords
        english_keyword_count = sum(1 for keyword in self.ENGLISH_KEYWORDS if keyword in content_lower)
        
        # If we find at least one English keyword, consider it English
        if english_keyword_count >= 1:
            return True
        
        # Additional check: look for ASCII text content (English is mostly ASCII)
        try:
            ascii_ratio = sum(1 for c in content if ord(c) < 128) / len(content)
            return ascii_ratio > 0.7  # More than 70% ASCII chars
        except:
            return False

    def has_valid_gherkin_steps(self, content: str) -> bool:
        """Check if feature file has valid Gherkin steps (given, when, then)."""
        if not content:
            return False
        
        content_lower = content.lower()
        
        # A valid feature file must have at least these Gherkin keywords
        has_given = "given" in content_lower
        has_when = "when" in content_lower
        has_then = "then" in content_lower
        
        # Require at least 2 out of 3 to be more lenient, or require all 3 for strict
        # Using strict approach: must have all three for valid test scenarios
        has_valid_steps = has_given and has_when and has_then
        
        return has_valid_steps

    def fetch_raw_feature_file(self, file_path: str) -> Optional[str]:
        """Download raw content of a feature file from GitHub."""
        raw_url = f"{self.raw_base_url}/{file_path}"

        try:
            resp = self.session.get(raw_url, timeout=10)
            if resp.status_code == 200:
                # Check if file is in English before saving
                if not self.is_english_feature_file(resp.text):
                    if self.verbose:
                        print(f"  ⏭️  Skipping non-English file: {file_path}")
                    self.skipped_non_english += 1
                    return None
                
                # Check if file has valid Gherkin steps (given, when, then)
                if not self.has_valid_gherkin_steps(resp.text):
                    if self.verbose:
                        print(f"  ⏭️  Skipping file without proper Gherkin steps: {file_path}")
                    self.skipped_non_english += 1  # Reusing counter for invalid files too
                    return None
                
                return resp.text
            else:
                return None
        except Exception as exc:
            self.errors.append(f"Error fetching raw file {file_path}: {exc}")
            return None

    def extract_file_paths_from_page(self, html: str, current_dir: str = "") -> List[str]:
        """
        Extract file/folder links from a GitHub web page.

        Returns list of relative paths to .feature files and folders.
        GitHub's HTML structure changed, so we need a more robust parser.
        """
        soup = BeautifulSoup(html, "html.parser")
        file_links = []
        found_items = set()  # Track items we've found to avoid duplicates

        # Method 1: Look for role="row" divs (current GitHub structure)
        for row in soup.find_all("div", {"role": "row"}):
            link_elem = row.find("a", href=True)
            if not link_elem:
                continue

            href = link_elem["href"]
            name = link_elem.get_text(strip=True)

            # Check if it's a .feature file
            if name.endswith(".feature"):
                if "/blob/" in href:
                    parts = href.split("/blob/", 1)
                    if len(parts) == 2:
                        path_part = parts[1]
                        # Remove branch from path
                        path_parts = path_part.split("/", 1)
                        if len(path_parts) == 2:
                            file_path = path_parts[1]
                            if file_path not in found_items:
                                file_links.append(("file", file_path))
                                found_items.add(file_path)
                            continue

            # Check if it's a folder/directory
            if "/tree/" in href:
                parts = href.split("/tree/", 1)
                if len(parts) == 2:
                    path_part = parts[1]
                    path_parts = path_part.split("/", 1)
                    if len(path_parts) == 2:
                        folder_path = path_parts[1]
                        if folder_path not in found_items:
                            file_links.append(("dir", folder_path))
                            found_items.add(folder_path)

        # Method 2: Fallback - look for all <a> tags with .feature or /tree/ in href
        # This catches items that might be missed by the structured parsing
        if not file_links:
            for link in soup.find_all("a", href=True):
                href = link["href"]
                text = link.get_text(strip=True)

                # Looking for .feature files
                if ".feature" in href and "/blob/" in href:
                    # Extract path after /blob/branch/
                    if f"{self.owner}/{self.repo}/blob/{self.branch}/" in href:
                        file_path = href.split(f"{self.owner}/{self.repo}/blob/{self.branch}/", 1)[1]
                        if file_path.endswith(".feature") and file_path not in found_items:
                            file_links.append(("file", file_path))
                            found_items.add(file_path)

                # Looking for directories
                elif f"{self.owner}/{self.repo}/tree/{self.branch}/" in href:
                    folder_path = href.split(f"{self.owner}/{self.repo}/tree/{self.branch}/", 1)[1]
                    if folder_path and folder_path not in found_items and not folder_path.endswith(".feature"):
                        file_links.append(("dir", folder_path))
                        found_items.add(folder_path)

        return file_links

    def scrape_directory(self, folder_path: str = "") -> None:
        """
        Recursively scrape a directory for .feature files.

        Args:
            folder_path: Path relative to repository root (empty for root)
        """
        # Build the URL for this directory
        if folder_path:
            url = f"{self.web_base_url}/{folder_path}"
        else:
            url = self.web_base_url

        # Avoid revisiting the same URL
        if url in self.visited_urls:
            return

        self.visited_urls.add(url)

        # Fetch the page
        html = self.get_page_html(url)
        if not html:
            self.errors.append(f"Failed to fetch {url}")
            return

        # Extract file and folder paths
        items = self.extract_file_paths_from_page(html)

        # Separate files and directories
        dirs_to_process = []
        files_to_download = []

        for item_type, item_path in items:
            if item_type == "file":
                files_to_download.append(item_path)
            elif item_type == "dir":
                dirs_to_process.append(item_path)

        # Download files
        if files_to_download:
            for file_path in files_to_download:
                self.download_feature_file(file_path)

        # Recursively scrape directories (will use thread pool in main scrape method)
        for dir_path in dirs_to_process:
            self.scrape_directory(dir_path)

    def scrape_parallel(self) -> None:
        """Scrape using parallel workers for faster processing."""
        # First, try to get all directories via API for comprehensive coverage
        api_directories = self.get_all_directories_api()
        
        # Queue of directories to process
        directories_queue = [""]  # Always start with root
        
        # Add API-discovered directories
        directories_queue.extend(api_directories)
        
        processed = set()

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            # Process root first to find initial structure via HTML
            initial_dirs = self._process_directory("")
            
            # Add HTML-discovered directories not already in the queue
            for dir_path in initial_dirs:
                if dir_path not in directories_queue:
                    directories_queue.append(dir_path)
            
            processed.add("")

            # Process remaining directories in parallel
            futures = {}
            
            while directories_queue or futures:
                # Submit new tasks to fill the worker pool
                while directories_queue and len(futures) < self.workers:
                    dir_path = directories_queue.pop(0)
                    if dir_path not in processed:
                        future = executor.submit(self._process_directory, dir_path)
                        futures[future] = dir_path
                        processed.add(dir_path)

                # Collect results as they complete (with longer timeout for validation)
                if futures:
                    try:
                        # Use longer timeout (30s) to allow for Gherkin validation processing
                        for future in as_completed(futures, timeout=30):
                            try:
                                new_dirs = future.result()
                                # Add new directories to queue if not processed
                                for d in new_dirs:
                                    if d not in processed:
                                        directories_queue.append(d)
                            except Exception as e:
                                self.errors.append(f"Error processing directory: {e}")
                            finally:
                                del futures[future]
                    except TimeoutError:
                        # Some futures still running, continue adding more work
                        continue


    def _process_directory(self, folder_path: str = "") -> List[str]:
        """
        Process a single directory and return subdirectories found.
        Returns list of subdirectories to process.
        """
        # Build the URL for this directory
        if folder_path:
            url = f"{self.web_base_url}/{folder_path}"
        else:
            url = self.web_base_url

        # Avoid revisiting the same URL
        if url in self.visited_urls:
            return []

        self.visited_urls.add(url)

        if self.verbose:
            print(f"📁 Processing: {folder_path or 'root'}")

        # Fetch the page
        html = self.get_page_html(url)
        if not html:
            error_msg = f"Failed to fetch {url}"
            self.errors.append(error_msg)
            if self.verbose:
                print(f"  ❌ {error_msg}")
            return []

        # Extract file and folder paths
        items = self.extract_file_paths_from_page(html)

        dirs_found = []

        for item_type, item_path in items:
            if item_type == "file":
                self.download_feature_file(item_path)
            elif item_type == "dir":
                dirs_found.append(item_path)

        return dirs_found

    def download_feature_file(self, file_path: str) -> None:
        """Download and save a feature file."""
        # Fetch the raw content
        content = self.fetch_raw_feature_file(file_path)
        if not content:
            self.errors.append(f"Failed to download {file_path}")
            return

        # Create local directory structure
        local_path = self.output_dir / file_path
        local_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the file
        try:
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.feature_files.append({
                "path": file_path,
                "local_path": str(local_path),
                "size": len(content),
                "lines": len(content.splitlines()),
            })
            
            # Update progress bar
            if self.pbar_files:
                self.pbar_files.update(1)
        except Exception as exc:
            self.errors.append(f"Failed to save {file_path}: {exc}")

    def scrape(self) -> Dict[str, object]:
        """Start the scraping process."""
        print("\n" + "=" * 80)
        print("GITHUB FEATURE FILE WEB SCRAPER (Parallel)")
        print("=" * 80 + "\n")
        
        print(f"🔧 Workers: {self.workers} (parallel processing for speed)")
        print(f"🌍 Language Filter: English-only (.feature files in other languages will be skipped)")
        
        if self.fresh_mode:
            print(f"🗑️  Mode: Fresh start (cleared old files)")
        else:
            print(f"📁 Mode: Append (adding to existing files)")
        
        print(f"🔍 Searching entire repository for .feature files...")
        print(f"   Using: HTML Parser + GitHub API (for complete coverage)")
        print(f"   Connection Pool: Optimized for high-performance batch mining\n")
        
        # Validate that the repository URL is accessible
        test_url = self.web_base_url
        if self.verbose:
            print(f"🔗 Testing repository access: {test_url}")
        
        test_html = self.get_page_html(test_url)
        
        if not test_html:
            print(f"❌ Repository not accessible at: {test_url}")
            print(f"\nTroubleshooting:")
            print(f"  1. Verify the repository exists: https://github.com/{self.owner}/{self.repo}")
            print(f"  2. Try specifying the branch explicitly:")
            print(f"     python3 github_feature_scraper.py 'https://github.com/{self.owner}/{self.repo}/tree/main'")
            print(f"  3. Use --verbose flag for more details")
            self.errors.append("Repository not accessible")
            self.print_summary()
            return {
                "repository": f"{self.owner}/{self.repo}",
                "branch": self.branch,
                "output_dir": str(self.output_dir),
                "total_feature_files": 0,
                "total_lines": 0,
                "total_size_bytes": 0,
                "feature_files": [],
                "errors": self.errors,
            }

        if self.verbose:
            print(f"✓ Repository accessible\n")
        else:
            print()

        # Use parallel scraping with progress bars
        with tqdm(total=0, desc="📄 Files", unit="file", leave=False) as pbar_files:
            self.pbar_files = pbar_files
            self.scrape_parallel()
            self.pbar_files = None

        # Generate summary
        self.print_summary()

        return {
            "repository": f"{self.owner}/{self.repo}",
            "branch": self.branch,
            "output_dir": str(self.output_dir),
            "total_feature_files": len(self.feature_files),
            "total_lines": sum(f["lines"] for f in self.feature_files),
            "total_size_bytes": sum(f["size"] for f in self.feature_files),
            "feature_files": self.feature_files,
            "errors": self.errors,
        }

    def print_summary(self) -> None:
        """Print scraping summary."""
        print("\n" + "=" * 80)
        print("SCRAPING SUMMARY")
        print("=" * 80)
        print(f"Repository: {self.owner}/{self.repo}")
        print(f"Branch: {self.branch}")
        print(f"Output Directory: {self.output_dir}")
        print(f"Directories Scanned: {len(self.visited_urls)}")
        print(f"\n✓ Feature Files Downloaded: {len(self.feature_files)}")
        if self.skipped_non_english > 0:
            print(f"⏭️  Non-English Files Skipped: {self.skipped_non_english}")

        if self.feature_files:
            total_lines = sum(f["lines"] for f in self.feature_files)
            total_size = sum(f["size"] for f in self.feature_files)
            print(f"✓ Total Lines: {total_lines:,}")
            print(f"✓ Total Size: {total_size:,} bytes")

            print(f"\nFeature Files:")
            for feature in self.feature_files[:10]:  # Show first 10
                print(f"  - {feature['path']} ({feature['lines']} lines)")

            if len(self.feature_files) > 10:
                print(f"  ... and {len(self.feature_files) - 10} more")
        else:
            # No files found - provide diagnostic info
            print(f"\n⚠️  No .feature files found!")
            print(f"\nDiagnostic Information:")
            print(f"  - URLs scanned: {len(self.visited_urls)}")
            if self.visited_urls:
                print(f"  - Sample URLs checked:")
                for url in list(self.visited_urls)[:5]:
                    print(f"    • {url}")
            print(f"\nTroubleshooting:")
            print(f"  1. Repository might not have .feature files")
            print(f"  2. Try --verbose flag to see detailed access logs:")
            print(f"     python3 github_feature_scraper.py ... --verbose")
            print(f"  3. Check repository exists and is public:")
            print(f"     https://github.com/{self.owner}/{self.repo}")

        if self.errors:
            print(f"\n⚠️  Errors ({len(self.errors)}):")
            for error in self.errors[:5]:
                print(f"  - {error}")

        print("=" * 80 + "\n")

    def save_manifest(self) -> None:
        """Save a manifest file with all scraped items."""
        import json

        manifest = {
            "repository": f"{self.owner}/{self.repo}",
            "branch": self.branch,
            "output_dir": str(self.output_dir),
            "total_feature_files": len(self.feature_files),
            "total_lines": sum(f["lines"] for f in self.feature_files),
            "total_size_bytes": sum(f["size"] for f in self.feature_files),
            "feature_files": self.feature_files,
            "errors": self.errors,
        }

        manifest_path = self.output_dir / "manifest.json"
        
        # Always merge with existing manifest (append is default)
        if manifest_path.exists() and not self.fresh_mode:
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                
                # Merge feature files (avoid duplicates by path)
                existing_paths = {f["path"] for f in existing.get("feature_files", [])}
                new_files = [f for f in self.feature_files if f["path"] not in existing_paths]
                
                merged_files = existing.get("feature_files", []) + new_files
                manifest["feature_files"] = merged_files
                manifest["total_feature_files"] = len(merged_files)
                manifest["total_lines"] = sum(f["lines"] for f in merged_files)
                manifest["total_size_bytes"] = sum(f["size"] for f in merged_files)
                manifest["errors"] = existing.get("errors", []) + self.errors
                
                num_added = len(new_files)
                num_existing = len(existing_paths)
                print(f"ℹ️  Merged: {num_added} new + {num_existing} existing = {len(merged_files)} total files")
            except Exception as e:
                print(f"⚠️  Could not merge with existing manifest: {e}")

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"✓ Manifest saved: {manifest_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape all .feature files from a GitHub repository (flexible URL formats)"
    )
    parser.add_argument(
        "repo_url",
        help="GitHub repository URL (supports multiple formats: https://github.com/owner/repo, owner/repo, https://github.com/owner/repo/tree/branch, etc.)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="scraped_features",
        help="Directory to save scraped feature files (default: scraped_features)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel workers for faster scraping (default: 8, recommended 4-16 for batch mining)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging to debug issues",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Start fresh: clear existing scraped files before scraping (default: append to existing files)",
    )

    args = parser.parse_args()
    
    # Validate workers (clamp to 1-16 range for optimal performance)
    workers = min(max(args.workers, 1), 16)

    try:
        scraper = GitHubFeatureScraper(args.repo_url, args.output_dir, workers=workers, verbose=args.verbose, fresh=args.fresh)
        result = scraper.scrape()
        scraper.save_manifest()

        print(f"\n✅ Scraping completed!")
        print(f"   Total feature files: {result['total_feature_files']}")
        print(f"   Output directory: {result['output_dir']}")
        
        if result['errors']:
            print(f"\n⚠️  Encountered {len(result['errors'])} error(s)")
            print("   Use --verbose flag for detailed information")

    except Exception as exc:
        print(f"\n❌ Error: {exc}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
