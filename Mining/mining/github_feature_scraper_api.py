"""
GitHub Feature File Scraper (API-based alternative - RECOMMENDED)

This is a more efficient alternative to the web scraper.
Uses GitHub API instead of web scraping for better performance and reliability.

Usage:
    export GITHUB_TOKEN=your_token  # Optional but recommended for higher rate limits
    python3 github_feature_scraper_api.py https://github.com/owner/repo/tree/branch
"""

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional

import requests


class GitHubFeatureScraperAPI:
    """Scrapes .feature files from GitHub using the GitHub API."""

    def __init__(self, repo_url: str, output_dir: str = "scraped_features"):
        """
        Initialize the API-based scraper.

        Args:
            repo_url: GitHub repository URL
            output_dir: Directory to save scraped feature files
        """
        self.repo_url = repo_url.rstrip("/")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Parse repository info from URL
        self.parse_repo_info()

        self.session = requests.Session()
        self.headers = {"Accept": "application/vnd.github+json"}

        # Use GitHub token if available
        token = os.getenv("GITHUB_TOKEN", "").strip()
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
            print("✓ Using GitHub token for authentication")
        else:
            print("⚠️  No GitHub token found. Using unauthenticated API (60 req/hr limit)")

        self.feature_files: List[Dict[str, str]] = []
        self.errors: List[str] = []

    def parse_repo_info(self) -> None:
        """Extract owner, repo name, and branch from GitHub URL."""
        match = re.search(r"github\.com/([^/]+)/([^/]+)(?:/tree/(.+)|/blob/(.+))?$", self.repo_url)

        if not match:
            raise ValueError(f"Invalid GitHub URL: {self.repo_url}")

        self.owner = match.group(1)
        self.repo = match.group(2)
        self.branch = match.group(3) or match.group(4) or "main"

        self.api_base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"

        print(f"Repository: {self.owner}/{self.repo}")
        print(f"Branch: {self.branch}\n")

    def get_tree_contents(self, path: str = "") -> Optional[List[Dict]]:
        """Get contents of a directory using GitHub API."""
        # Use the /contents endpoint for directories
        url = f"{self.api_base_url}/contents/{path}" if path else f"{self.api_base_url}/contents"

        params = {"ref": self.branch}

        try:
            resp = self.session.get(url, headers=self.headers, params=params, timeout=10)

            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                return None
            else:
                print(f"  ⚠️  API error {resp.status_code}: {resp.text[:200]}")
                return None

        except Exception as exc:
            print(f"  ⚠️  Error fetching {path}: {exc}")
            return None

    def download_feature_file(self, file_item: Dict) -> bool:
        """Download a feature file from GitHub."""
        file_path = file_item["path"]
        download_url = file_item["download_url"]

        print(f"  📄 Downloading: {file_path}")

        try:
            resp = self.session.get(download_url, timeout=10)

            if resp.status_code != 200:
                print(f"    ✗ Failed to download: {resp.status_code}")
                self.errors.append(f"Failed to download {file_path}: {resp.status_code}")
                return False

            content = resp.text

            # Create local directory structure
            local_path = self.output_dir / file_path
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Save the file
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.feature_files.append({
                "path": file_path,
                "local_path": str(local_path),
                "size": len(content),
                "lines": len(content.splitlines()),
                "download_url": download_url,
            })

            return True

        except Exception as exc:
            print(f"    ✗ Error saving {file_path}: {exc}")
            self.errors.append(f"Failed to save {file_path}: {exc}")
            return False

    def scrape_directory(self, path: str = "") -> None:
        """Recursively scrape a directory for .feature files."""
        print(f"Scraping: {path or 'root'}...")

        contents = self.get_tree_contents(path)
        if contents is None:
            return

        for item in contents:
            if item["type"] == "file" and item["name"].endswith(".feature"):
                # Download the feature file
                self.download_feature_file(item)
                time.sleep(0.2)  # Rate limiting

            elif item["type"] == "dir":
                # Recursively scrape directory
                self.scrape_directory(item["path"])

    def scrape(self) -> Dict[str, object]:
        """Start the scraping process."""
        print("\n" + "=" * 80)
        print("GITHUB FEATURE FILE SCRAPER (API-based)")
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

            print(f"\nTop Feature Files:")
            sorted_files = sorted(self.feature_files, key=lambda x: x["lines"], reverse=True)
            for feature in sorted_files[:10]:
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
        description="Scrape all .feature files from GitHub using the GitHub API (RECOMMENDED)"
    )
    parser.add_argument(
        "repo_url",
        help="GitHub repository URL (e.g., https://github.com/owner/repo/tree/branch)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="scraped_features",
        help="Directory to save scraped feature files",
    )

    args = parser.parse_args()

    try:
        scraper = GitHubFeatureScraperAPI(args.repo_url, args.output_dir)
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
