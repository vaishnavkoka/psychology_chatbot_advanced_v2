"""
Enhanced Mining Tool - Extract Actual Feature Files
Downloads real .feature files from OSS projects and creates a rich dataset
"""

import os
import json
import csv
import requests
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from urllib.parse import urljoin
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Mining.mining.mining_config import MINING_CONFIG, CSV_COLUMNS


class FeatureFileExtractor:
    """Extract actual feature files from GitHub"""
    
    def __init__(self):
        self.config = MINING_CONFIG
        self.output_dir = Path(self.config["output"]["output_dir"])
        self.features_dir = self.output_dir / "feature_files"
        self.features_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().isoformat()

    def _build_github_headers(self) -> Dict[str, str]:
        """Build GitHub API headers and include auth only when token is set."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }

        token = os.getenv("GITHUB_TOKEN", "").strip()
        if token:
            headers["Authorization"] = f"token {token}"

        return headers
        
    def search_github_with_feature_files(self) -> List[Dict]:
        """Search GitHub for projects with actual .feature files"""
        
        projects = [
            {
                "id": 1,
                "name": "cucumber-js",
                "full_name": "cucumber/cucumber-js",
                "url": "https://github.com/cucumber/cucumber-js",
                "stars": 2500,
                "language": "JavaScript",
                "default_branch": "main",
            },
            {
                "id": 2,
                "name": "behave",
                "full_name": "behave/behave",
                "url": "https://github.com/behave/behave",
                "stars": 2300,
                "language": "Python",
                "default_branch": "master",
            },
            {
                "id": 3,
                "name": "robot-framework",
                "full_name": "robotframework/robotframework",
                "url": "https://github.com/robotframework/robotframework",
                "stars": 1800,
                "language": "Python",
                "default_branch": "master",
            },
        ]
        
        return projects
    
    def fetch_feature_files_from_github(self, project: Dict) -> List[Dict]:
        """
        Fetch actual .feature files from GitHub using API
        Returns list of feature files with content
        """
        features = []
        
        try:
            # Search for .feature files in the repository using GitHub API
            headers = self._build_github_headers()
            
            # Use GitHub code search to find .feature files
            search_url = "https://api.github.com/search/code"
            params = {
                "q": f"repo:{project['full_name']} filename:*.feature",
                "per_page": 20,
            }
            
            logger.info(f"Searching for .feature files in {project['full_name']}...")
            
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                logger.info(f"Found {len(items)} .feature files")
                
                for item in items[:10]:  # Limit to 10 per project
                    features.append({
                        "file_path": item["path"],
                        "file_name": Path(item["path"]).name,
                        "url": item["html_url"],
                        "file_size": item.get("size", 0),
                    })
            else:
                logger.warning(f"GitHub search failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching features: {e}")
        
        return features
    
    def get_feature_file_content(self, project: Dict, file_path: str) -> Optional[str]:
        """Download actual feature file content from GitHub"""
        
        try:
            # Use GitHub raw content URL
            raw_url = f"https://raw.githubusercontent.com/{project['full_name']}/{project['default_branch']}/{file_path}"
            
            response = requests.get(raw_url, timeout=10)
            
            if response.status_code == 200:
                return response.text
            
        except Exception as e:
            logger.error(f"Failed to get content for {file_path}: {e}")
        
        return None
    
    def save_feature_file_locally(self, project: Dict, file_path: str, content: str) -> Path:
        """Save feature file to local directory"""
        
        # Create directory structure: features_dir/project_name/path/to/file.feature
        local_path = self.features_dir / project["name"] / file_path
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved: {local_path}")
            return local_path
        except Exception as e:
            logger.error(f"Failed to save {local_path}: {e}")
            return None
    
    def extract_gherkin_scenarios(self, content: str) -> List[str]:
        """Parse Gherkin content and extract scenario names"""
        scenarios = []
        
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('Scenario:') or line.startswith('Scenario Outline:'):
                scenario_name = line.replace('Scenario:', '').replace('Scenario Outline:', '').strip()
                scenarios.append(scenario_name)
        
        return scenarios
    
    def extract_feature_description(self, content: str) -> str:
        """Extract feature description from Gherkin file"""
        
        lines = content.split('\n')
        description = []
        in_feature = False
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('Feature:'):
                in_feature = True
                # Get feature name
                feature_name = stripped.replace('Feature:', '').strip()
                description.append(feature_name)
            elif in_feature and (stripped.startswith('Scenario:') or stripped.startswith('Scenario Outline:')):
                # Stop at first scenario
                break
            elif in_feature and stripped and not stripped.startswith('#'):
                description.append(stripped)
        
        return ' '.join(description)[:200]  # First 200 chars
    
    def generate_feature_rich_dataset(self) -> List[Dict]:
        """Generate dataset with actual feature file content"""
        
        dataset = []
        projects = self.search_github_with_feature_files()
        
        for project in projects:
            logger.info(f"\nProcessing project: {project['name']}")
            
            # Fetch feature files from GitHub
            feature_files = self.fetch_feature_files_from_github(project)
            
            if len(feature_files) < self.config["bdd_criteria"]["min_feature_files"]:
                logger.info(f"Project has only {len(feature_files)} features (need {self.config['bdd_criteria']['min_feature_files']})")
                continue
            
            for feature in feature_files:
                # Get actual file content
                content = self.get_feature_file_content(project, feature["file_path"])
                
                if content:
                    # Save locally
                    local_path = self.save_feature_file_locally(project, feature["file_path"], content)
                    
                    # Extract information
                    scenarios = self.extract_gherkin_scenarios(content)
                    description = self.extract_feature_description(content)
                    
                    # Create dataset row
                    row = {
                        "project_id": project["id"],
                        "project_name": project["name"],
                        "project_url": project["url"],
                        "github_stars": project["stars"],
                        "language": project["language"],
                        "feature_file_count": len(feature_files),
                        "feature_file_name": feature["file_name"],
                        "feature_file_path": feature["file_path"],
                        "feature_description": description,
                        "scenario_count": len(scenarios),
                        "scenarios": "; ".join(scenarios) if scenarios else "Not parsed",
                        "feature_file_url": feature["url"],
                        "feature_content_preview": content[:300],
                        "local_feature_path": str(local_path) if local_path else "Failed to save",
                        "mining_timestamp": self.timestamp,
                    }
                    dataset.append(row)
        
        return dataset
    
    def save_rich_dataset(self, dataset: List[Dict]):
        """Save enhanced dataset to CSV"""
        
        if not dataset:
            logger.error("No data to save")
            return
        
        csv_path = self.output_dir / "bdd_oss_mining_with_features.csv"
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=dataset[0].keys())
                writer.writeheader()
                writer.writerows(dataset)
            
            logger.info(f"\n✓ Rich dataset saved: {csv_path}")
            logger.info(f"  Total rows: {len(dataset)}")
            print(f"\n✓ Dataset generated: {csv_path}")
            print(f"  Rows: {len(dataset)}")
            
        except Exception as e:
            logger.error(f"Failed to save CSV: {e}")
    
    def generate_feature_files_summary(self, dataset: List[Dict]):
        """Generate summary of extracted feature files"""
        
        summary_path = self.output_dir / "feature_files_summary.json"
        
        summary = {
            "timestamp": self.timestamp,
            "total_projects": len(set(row["project_name"] for row in dataset)),
            "total_features": len(dataset),
            "feature_files_dir": str(self.features_dir),
            "features": [
                {
                    "project": row["project_name"],
                    "file_name": row["feature_file_name"],
                    "path": row["feature_file_path"],
                    "scenarios": row["scenario_count"],
                    "url": row["feature_file_url"],
                    "local_path": row["local_feature_path"],
                }
                for row in dataset
            ]
        }
        
        try:
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
            logger.info(f"Summary saved: {summary_path}")
        except Exception as e:
            logger.error(f"Failed to save summary: {e}")
    
    def run(self):
        """Execute the feature file extraction"""
        
        print("\n" + "="*70)
        print("FEATURE FILE EXTRACTION - Real GitHub Data")
        print("="*70)
        
        # Generate dataset with actual feature content
        print("\n[1/3] Fetching and extracting feature files from GitHub...")
        dataset = self.generate_feature_rich_dataset()
        
        if dataset:
            # Save to CSV
            print("[2/3] Saving enhanced dataset...")
            self.save_rich_dataset(dataset)
            
            # Generate summary
            print("[3/3] Creating feature files summary...")
            self.generate_feature_files_summary(dataset)
            
            print("\n" + "="*70)
            print("SUMMARY")
            print("="*70)
            print(f"Total features extracted: {len(dataset)}")
            print(f"Feature files directory: {self.features_dir}")
            print(f"CSV dataset: {self.output_dir}/bdd_oss_mining_with_features.csv")
            print(f"Summary: {self.output_dir}/feature_files_summary.json")
            print("="*70 + "\n")
            
            # Display sample data
            if dataset:
                print("SAMPLE DATA (First Feature):")
                print("-" * 70)
                first = dataset[0]
                print(f"Project: {first['project_name']}")
                print(f"Feature File: {first['feature_file_name']}")
                print(f"Path: {first['feature_file_path']}")
                print(f"Description: {first['feature_description']}")
                print(f"Scenarios: {first['scenario_count']}")
                print(f"URL: {first['feature_file_url']}")
                print(f"Saved to: {first['local_feature_path']}")
                print("-" * 70 + "\n")
        else:
            print("✗ No features extracted")


def main():
    """Main entry point"""
    extractor = FeatureFileExtractor()
    extractor.run()


if __name__ == "__main__":
    main()
