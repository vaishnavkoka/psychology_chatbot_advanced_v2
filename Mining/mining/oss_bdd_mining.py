"""
OSS BDD Mining Tool - Main Mining Pipeline
Mines open source software projects for BDD artifacts (feature files, step definitions, requirements)
and creates a structured CSV dataset.

Author: Mining Pipeline
Purpose: Extract BDD test artifacts from GitHub OSS projects
"""

import os
import json
import csv
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import requests
from urllib.parse import urljoin
import tempfile
import glob
import logging

from Mining.mining.mining_config import MINING_CONFIG, CSV_COLUMNS, GITHUB_SEARCH_QUERIES

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BDDMiningPipeline:
    """Main pipeline for mining BDD artifacts from OSS projects"""
    
    def __init__(self, use_mock_data: bool = False):
        """
        Initialize the mining pipeline
        
        Args:
            use_mock_data: If True, use mock data for pilot testing
        """
        self.config = MINING_CONFIG
        self.use_mock_data = use_mock_data
        self.output_dir = Path(self.config["output"]["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().isoformat()
        self.mining_results = []
        self.projects_scanned = 0
        self.valid_projects = 0

    def _build_github_headers(self) -> Dict[str, str]:
        """Build GitHub API headers and include auth only when token is set."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }

        token = os.getenv("GITHUB_TOKEN", "").strip()
        if token:
            headers["Authorization"] = f"token {token}"

        return headers
        
    def search_github_projects(self) -> List[Dict]:
        """
        Search GitHub for projects with BDD feature files
        
        Returns:
            List of project metadata dictionaries
        """
        if self.use_mock_data:
            logger.info("Using mock data for pilot (GitHub API not called)")
            return self._get_mock_projects()
        
        projects = []
        headers = self._build_github_headers()
        
        logger.info("Searching GitHub for BDD projects...")
        
        for query in GITHUB_SEARCH_QUERIES[:2]:  # Limit queries for pilot
            try:
                url = f"{self.config['github']['base_api_url']}/search/repositories"
                params = {
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": min(30, self.config["pilot_limits"]["max_projects_to_scan"]),
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                for repo in data.get("items", [])[:10]:  # Limit to 10 per query
                    projects.append({
                        "id": repo["id"],
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "url": repo["html_url"],
                        "clone_url": repo["clone_url"],
                        "stars": repo["stargazers_count"],
                        "language": repo["language"],
                        "description": repo["description"],
                    })
                
                logger.info(f"Found {len(projects)} projects from query: {query[:50]}")
                
            except Exception as e:
                logger.error(f"Error searching GitHub: {e}")
        
        return projects[:self.config["pilot_limits"]["max_projects_to_scan"]]
    
    def _get_mock_projects(self) -> List[Dict]:
        """Get mock project data for pilot testing"""
        return [
            {
                "id": 1,
                "name": "cucumber-js",
                "full_name": "cucumber/cucumber-js",
                "url": "https://github.com/cucumber/cucumber-js",
                "clone_url": "https://github.com/cucumber/cucumber-js.git",
                "stars": 2500,
                "language": "JavaScript",
                "description": "Cucumber for JavaScript",
            },
            {
                "id": 2,
                "name": "behave",
                "full_name": "behave/behave",
                "url": "https://github.com/behave/behave",
                "clone_url": "https://github.com/behave/behave.git",
                "stars": 2300,
                "language": "Python",
                "description": "BDD framework for Python",
            },
            {
                "id": 3,
                "name": "gherkin",
                "full_name": "cucumber/gherkin",
                "url": "https://github.com/cucumber/gherkin",
                "clone_url": "https://github.com/cucumber/gherkin.git",
                "stars": 1800,
                "language": "Java",
                "description": "Gherkin parser",
            },
        ]
    
    def clone_and_analyze_project(self, project: Dict) -> Optional[Dict]:
        """
        Clone a project and extract BDD artifacts
        
        Args:
            project: Project metadata dictionary
            
        Returns:
            Analysis results or None if project doesn't meet criteria
        """
        temp_dir = None
        try:
            # Create temp directory
            temp_dir = tempfile.mkdtemp(prefix="bdd_mining_")
            project_path = Path(temp_dir)
            
            logger.info(f"Cloning {project['full_name']}...")
            
            # Clone repository with limited depth to save time
            result = subprocess.run(
                ["git", "clone", "--depth", "1", project["clone_url"], str(project_path)],
                timeout=self.config["pilot_limits"]["clone_timeout_seconds"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.warning(f"Failed to clone {project['full_name']}: {result.stderr}")
                return None
            
            # Extract BDD artifacts
            artifacts = self._extract_bdd_artifacts(project_path, project)
            
            if not artifacts:
                logger.info(f"No BDD artifacts found in {project['full_name']}")
                return None
            
            return artifacts
            
        except subprocess.TimeoutExpired:
            logger.warning(f"Clone timeout for {project['full_name']}")
            return None
        except Exception as e:
            logger.error(f"Error analyzing {project['full_name']}: {e}")
            return None
        finally:
            # Cleanup temp directory
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp dir: {e}")
    
    def _extract_bdd_artifacts(self, project_path: Path, project: Dict) -> Optional[Dict]:
        """
        Extract feature files, step definitions, and requirements from project
        
        Args:
            project_path: Path to cloned repository
            project: Project metadata
            
        Returns:
            Extracted artifacts or None
        """
        # Find feature files
        feature_files = self._find_files(project_path, "*.feature")
        
        if len(feature_files) < self.config["bdd_criteria"]["min_feature_files"]:
            logger.info(f"Project has only {len(feature_files)} feature files (need {self.config['bdd_criteria']['min_feature_files']})")
            return None
        
        logger.info(f"Found {len(feature_files)} feature files")
        
        # Find step definitions
        step_defs = self._find_step_definitions(project_path)
        
        # Extract requirements
        requirements = self._extract_requirements(project_path)
        
        return {
            "project": project,
            "feature_files": feature_files[:self.config["pilot_limits"]["max_feature_files_per_project"]],
            "step_definitions": step_defs,
            "requirements": requirements,
            "feature_count": len(feature_files),
        }
    
    def _find_files(self, base_path: Path, pattern: str) -> List[Path]:
        """Find files matching pattern"""
        files = []
        try:
            files = list(base_path.rglob(pattern))
        except PermissionError:
            logger.warning(f"Permission denied searching {base_path}")
        return files
    
    def _find_step_definitions(self, project_path: Path) -> Dict[str, List[str]]:
        """Find step definition files"""
        step_defs = {
            "python": [],
            "javascript": [],
            "java": [],
            "ruby": [],
        }
        
        patterns = {
            "python": "*step*.py",
            "javascript": "*step*.js",
            "java": "*Step*.java",
            "ruby": "*spec*.rb",
        }
        
        for lang, pattern in patterns.items():
            files = self._find_files(project_path, pattern)
            step_defs[lang] = [str(f.relative_to(project_path)) for f in files[:10]]
        
        return step_defs
    
    def _extract_requirements(self, project_path: Path) -> List[Dict]:
        """Extract requirements from project"""
        requirements = []
        
        # Look for requirements files
        req_files = (
            self._find_files(project_path, "requirements.txt") +
            self._find_files(project_path, "requirements.md") +
            self._find_files(project_path, "README.md")
        )
        
        for req_file in req_files[:3]:
            try:
                with open(req_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Extract first 500 chars as requirement summary
                    requirements.append({
                        "file": str(req_file.relative_to(project_path)),
                        "content_preview": content[:300],
                    })
            except Exception as e:
                logger.warning(f"Failed to read {req_file}: {e}")
        
        return requirements
    
    def generate_csv_dataset(self):
        """Generate CSV dataset from mining results"""
        csv_path = self.output_dir / self.config["output"]["dataset_filename"]
        
        rows = []
        for result in self.mining_results:
            project = result["project"]
            features = result["feature_files"]
            requirements = result["requirements"]
            step_defs = result["step_definitions"]
            
            # Create one row per feature file and requirement combination
            for feature_file in features:
                for requirement in requirements or [{"file": "N/A", "content_preview": ""}]:
                    step_lang = "multiple" if any(step_defs.values()) else "not_found"
                    
                    row = {
                        "project_id": project["id"],
                        "project_name": project["name"],
                        "project_url": project["url"],
                        "github_stars": project["stars"],
                        "language": project.get("language", "Unknown"),
                        "feature_file_count": result["feature_count"],
                        "feature_file_name": feature_file.name,
                        "requirement_id": requirement.get("file", "N/A"),
                        "requirement_text": requirement.get("content_preview", "")[:100],
                        "step_definitions_found": any(step_defs.values()),
                        "step_definitions_language": step_lang,
                        "feature_file_url": project["url"] + f"/blob/main/{feature_file.relative_to(feature_file.parent.parent.parent)}",
                        "step_definitions_url": project["url"],
                        "mining_timestamp": self.timestamp,
                    }
                    rows.append(row)
        
        # Write CSV
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
                writer.writeheader()
                writer.writerows(rows)
            
            logger.info(f"Dataset saved to {csv_path} with {len(rows)} rows")
            print(f"\n✓ Dataset generated: {csv_path}")
            print(f"  Total rows: {len(rows)}")
            
        except Exception as e:
            logger.error(f"Failed to generate CSV: {e}")
    
    def save_metadata(self):
        """Save mining metadata"""
        metadata = {
            "timestamp": self.timestamp,
            "total_projects_scanned": self.projects_scanned,
            "valid_projects_found": self.valid_projects,
            "total_features_extracted": len(self.mining_results),
            "output_file": str(self.output_dir / self.config["output"]["dataset_filename"]),
            "config": self.config,
        }
        
        metadata_path = self.output_dir / self.config["output"]["metadata_filename"]
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Metadata saved to {metadata_path}")
    
    def run_mining_pipeline(self):
        """Execute the complete mining pipeline"""
        logger.info("Starting BDD Mining Pipeline...")
        print("\n" + "="*60)
        print("OSS BDD MINING PIPELINE - PILOT RUN")
        print("="*60)
        
        # Step 1: Search for projects
        print("\n[Step 1/4] Searching for BDD projects...")
        projects = self.search_github_projects()
        print(f"✓ Found {len(projects)} candidate projects")
        
        # Step 2: Clone and analyze projects
        print("\n[Step 2/4] Cloning and analyzing projects...")
        for i, project in enumerate(projects, 1):
            print(f"  [{i}/{len(projects)}] {project['full_name']}... ", end="", flush=True)
            self.projects_scanned += 1
            
            result = self.clone_and_analyze_project(project)
            if result:
                self.mining_results.append(result)
                self.valid_projects += 1
                print(f"✓ ({result['feature_count']} features)")
            else:
                print("✗")
        
        # Step 3: Generate dataset
        print("\n[Step 3/4] Generating CSV dataset...")
        self.generate_csv_dataset()
        
        # Step 4: Save metadata
        print("[Step 4/4] Saving metadata...")
        self.save_metadata()
        
        # Print summary
        print("\n" + "="*60)
        print("MINING SUMMARY")
        print("="*60)
        print(f"Projects scanned: {self.projects_scanned}")
        print(f"Valid projects found: {self.valid_projects}")
        print(f"Feature files extracted: {sum(r['feature_count'] for r in self.mining_results)}")
        print(f"Output directory: {self.output_dir}")
        print("="*60 + "\n")


def main():
    """Main entry point"""
    # Toggle with USE_MOCK_DATA=true/false (defaults to false for real mining).
    use_mock_data = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
    pipeline = BDDMiningPipeline(use_mock_data=use_mock_data)
    pipeline.run_mining_pipeline()


if __name__ == "__main__":
    main()
