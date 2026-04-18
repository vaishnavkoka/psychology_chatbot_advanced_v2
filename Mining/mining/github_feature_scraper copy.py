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
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class GitHubFeatureScraper:
    """Scrapes .feature files from GitHub repositories using BeautifulSoup."""

    def __init__(self, repo_url: str, output_dir: str = "scraped_features"):
        """
        Initialize the scraper.

        Args:
            repo_url: GitHub repository URL (e.g., https://github.com/user/repo/tree/branch)
            output_dir: Directory to save scraped feature files
        """
        self.repo_url = repo_url.rstrip("/")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Parse repository info from URL
        self.parse_repo_info()

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

        self.visited_urls: Set[str] = set()
        self.feature_files: List[Dict[str, str]] = []
        self.errors: List[str] = []

    def parse_repo_info(self) -> None:
        """Extract owner, repo name, and branch from GitHub URL."""
        # Pattern: https://github.com/owner/repo/tree/branch or /blob/...
        match = re.search(r"github\.com/([^/]+)/([^/]+)(?:/tree/(.+)|/blob/(.+))?$", self.repo_url)

        if not match:
            raise ValueError(f"Invalid GitHub URL: {self.repo_url}")

        self.owner = match.group(1)
        self.repo = match.group(2)
        self.branch = match.group(3) or match.group(4) or "main"

        # Construct the raw content base URL for this repo
        self.raw_base_url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}"
        self.web_base_url = f"https://github.com/{self.owner}/{self.repo}/tree/{self.branch}"

        print(f"Repository: {self.owner}/{self.repo}")
        print(f"Branch: {self.branch}")
        print(f"Web Base URL: {self.web_base_url}\n")

    def get_page_html(self, url: str) -> Optional[str]:
        """Fetch HTML content from a GitHub URL."""
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.text
            else:
                print(f"  ⚠️  Failed to fetch {url}: {resp.status_code}")
                return None
        except Exception as exc:
            print(f"  ⚠️  Error fetching {url}: {exc}")
            return None

    def fetch_raw_feature_file(self, file_path: str) -> Optional[str]:
        """Download raw content of a feature file from GitHub."""
        raw_url = f"{self.raw_base_url}/{file_path}"

        try:
            resp = self.session.get(raw_url, timeout=10)
            if resp.status_code == 200:
                return resp.text
            else:
                return None
        except Exception as exc:
            print(f"  ⚠️  Error fetching raw file {file_path}: {exc}")
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

        print(f"Scraping: {folder_path or 'root'}...")

        # Fetch the page
        html = self.get_page_html(url)
        if not html:
            self.errors.append(f"Failed to fetch {url}")
            return

        # Extract file and folder paths
        items = self.extract_file_paths_from_page(html)

        for item_type, item_path in items:
            if item_type == "file":
                # Download the feature file
                self.download_feature_file(item_path)

            elif item_type == "dir":
                # Recursively scrape the directory
                time.sleep(0.5)  # Rate limiting
                self.scrape_directory(item_path)

    def download_feature_file(self, file_path: str) -> None:
        """Download and save a feature file."""
        print(f"  📄 Downloading: {file_path}")

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
        except Exception as exc:
            print(f"    ✗ Error saving {file_path}: {exc}")
            self.errors.append(f"Failed to save {file_path}: {exc}")

    def scrape(self) -> Dict[str, object]:
        """Start the scraping process."""
        print("\n" + "=" * 80)
        print("GITHUB FEATURE FILE WEB SCRAPER")
        print("=" * 80 + "\n")

        self.scrape_directory()

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
        print(f"\n✓ Feature Files Downloaded: {len(self.feature_files)}")

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
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"✓ Manifest saved: {manifest_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape all .feature files from a GitHub repository using BeautifulSoup"
    )
    parser.add_argument(
        "repo_url",
        help="GitHub repository URL (e.g., https://github.com/owner/repo/tree/branch)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="scraped_features",
        help="Directory to save scraped feature files (default: scraped_features)",
    )

    args = parser.parse_args()

    try:
        scraper = GitHubFeatureScraper(args.repo_url, args.output_dir)
        result = scraper.scrape()
        scraper.save_manifest()

        print(f"\n✅ Scraping completed!")
        print(f"   Total feature files: {result['total_feature_files']}")
        print(f"   Output directory: {result['output_dir']}")

    except Exception as exc:
        print(f"\n❌ Error: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
