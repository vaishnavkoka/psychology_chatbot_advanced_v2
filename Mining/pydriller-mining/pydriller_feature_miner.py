"""
PyDriller-based BDD Feature Mining Tool
Mines Git repositories to extract Gherkin BDD scenarios and analyze their evolution
Enhanced mining with full Git history, commit metadata, and feature evolution tracking
"""

import os
import json
import csv
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Set
import tempfile
import shutil
from collections import defaultdict

from pydriller import Repository, Commit
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from Mining.mining.mining_config import MINING_CONFIG


class PyDrillerFeatureMiner:
    """Mine BDD features from Git repositories using PyDriller"""
    
    def __init__(self, output_prefix: str = "pydriller"):
        self.output_dir = Path(MINING_CONFIG["output"]["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_prefix = output_prefix
        self.timestamp = datetime.now().isoformat()
        self.repositories_mined = []
        self.features_extracted = []
        self.feature_commits = defaultdict(list)
        self.stats = {
            "total_repositories": 0,
            "total_commits_analyzed": 0,
            "total_feature_files_found": 0,
            "total_scenarios_extracted": 0,
            "total_commits_with_features": 0,
        }
        
    def mine_repository(self, repo_url: str, repo_name: str, branch: str = "main") -> Dict:
        """
        Mine a Git repository for BDD feature files and their evolution
        
        Args:
            repo_url: GitHub repository URL
            repo_name: Human-readable repository name
            branch: Git branch to analyze
            
        Returns:
            Dictionary with mining results
        """
        print(f"\n🔍 Mining repository: {repo_name}")
        print(f"   URL: {repo_url}")
        print(f"   Branch: {branch}")
        
        try:
            # Initialize repository with just the URL
            # PyDriller 2.9 simpler API - will analyze all commits
            repo = Repository(repo_url)
            
            repo_data = {
                "repo_url": repo_url,
                "repo_name": repo_name,
                "branch": branch,
                "commits_analyzed": 0,
                "feature_files": [],
                "total_scenarios": 0,
                "first_commit": None,
                "last_commit": None,
                "commits_with_features": 0,
                "languages_in_steps": set(),
            }
            
            features_by_file = defaultdict(lambda: {
                "scenarios": [],
                "commits": [],
                "first_seen": None,
                "last_modified": None,
                "history": []
            })
            
            commit_count = 0
            
            for commit in repo.traverse_commits():
                commit_count += 1
                repo_data["commits_analyzed"] = commit_count
                
                # Track first and last commits
                if repo_data["first_commit"] is None:
                    repo_data["first_commit"] = self._format_commit_info(commit)
                repo_data["last_commit"] = self._format_commit_info(commit)
                
                # Check for .feature files modified in this commit
                for modified_file in commit.modified_files:
                    if modified_file.filename.endswith(".feature"):
                        repo_data["commits_with_features"] += 1
                        self.stats["total_commits_with_features"] += 1
                        feature_path = modified_file.filename
                        
                        # Extract scenarios from file changes
                        scenarios = self._extract_scenarios_from_diff(
                            modified_file.source_code,
                            modified_file.filename
                        )
                        
                        if scenarios:
                            features_by_file[feature_path]["scenarios"].extend(scenarios)
                            features_by_file[feature_path]["commits"].append({
                                "hash": commit.hash[:8],
                                "author": commit.author.name,
                                "date": commit.committer_date.isoformat(),
                                "message": commit.msg.split('\n')[0][:100],
                                "added_lines": modified_file.added_lines,
                                "deleted_lines": modified_file.deleted_lines,
                            })
                            
                            if features_by_file[feature_path]["first_seen"] is None:
                                features_by_file[feature_path]["first_seen"] = commit.committer_date.isoformat()
                            
                            features_by_file[feature_path]["last_modified"] = commit.committer_date.isoformat()
                
                # Find step definition files
                for modified_file in commit.modified_files:
                    if self._is_step_definition(modified_file.filename):
                        lang = self._detect_language(modified_file.filename)
                        if lang:
                            repo_data["languages_in_steps"].add(lang)
            
            # Process and organize features
            for feature_path, feature_data in features_by_file.items():
                # Deduplicate scenarios
                unique_scenarios = list(set(feature_data["scenarios"]))
                
                feature_info = {
                    "file_path": feature_path,
                    "scenario_count": len(unique_scenarios),
                    "scenarios": unique_scenarios,
                    "commits_count": len(feature_data["commits"]),
                    "first_seen": feature_data["first_seen"],
                    "last_modified": feature_data["last_modified"],
                    "commit_history": feature_data["commits"][:10],  # Last 10 commits
                    "authors": list(set([c["author"] for c in feature_data["commits"]]))
                }
                
                repo_data["feature_files"].append(feature_info)
                repo_data["total_scenarios"] += len(unique_scenarios)
                
                self.features_extracted.append({
                    "repo_name": repo_name,
                    "feature_file": feature_path,
                    "scenario_count": len(unique_scenarios),
                    "scenarios": " | ".join(unique_scenarios),
                    "commits": len(feature_data["commits"]),
                    "first_seen": feature_data["first_seen"],
                    "last_modified": feature_data["last_modified"],
                })
            
            repo_data["languages_in_steps"] = list(repo_data["languages_in_steps"])
            self.repositories_mined.append(repo_data)
            
            # Update stats
            self.stats["total_repositories"] += 1
            self.stats["total_commits_analyzed"] += commit_count
            self.stats["total_feature_files_found"] += len(repo_data["feature_files"])
            self.stats["total_scenarios_extracted"] += repo_data["total_scenarios"]
            
            print(f"   ✓ Analyzed {commit_count} commits")
            print(f"   ✓ Found {len(repo_data['feature_files'])} feature files")
            print(f"   ✓ Extracted {repo_data['total_scenarios']} scenarios")
            
            return repo_data
            
        except Exception as e:
            print(f"   ❌ Error mining repository: {str(e)}")
            return None
    
    def mine_multiple_repositories(self, repositories: List[Dict]) -> None:
        """
        Mine multiple repositories
        
        Args:
            repositories: List of repo configs with 'url', 'name', 'branch' keys
        """
        print(f"\n{'='*80}")
        print(f"🚀 PyDriller BDD Feature Mining")
        print(f"{'='*80}")
        
        for repo_config in repositories:
            try:
                self.mine_repository(
                    repo_url=repo_config["url"],
                    repo_name=repo_config["name"],
                    branch=repo_config.get("branch", "main")
                )
            except Exception as e:
                print(f"   ❌ Failed to mine {repo_config['name']}: {str(e)}")
                continue
        
        self._export_results()
    
    def _extract_scenarios_from_diff(self, source_code: Optional[str], filename: str) -> List[str]:
        """
        Extract Gherkin scenario names from feature file content
        """
        if source_code is None:
            return []
        
        scenarios = []
        
        # Match Scenario: <name>
        scenario_pattern = r'Scenario[:\s]+(.+?)(?:\n|$)'
        matches = re.findall(scenario_pattern, source_code, re.IGNORECASE)
        scenarios.extend([m.strip() for m in matches if m.strip()])
        
        # Match Scenario Outline: <name>
        outline_pattern = r'Scenario Outline[:\s]+(.+?)(?:\n|$)'
        matches = re.findall(outline_pattern, source_code, re.IGNORECASE)
        scenarios.extend([m.strip() for m in matches if m.strip()])
        
        return scenarios
    
    def _is_step_definition(self, filename: str) -> bool:
        """Check if file appears to be step definitions"""
        step_patterns = MINING_CONFIG["bdd_criteria"]["step_definition_patterns"]
        return any(re.match(pattern, filename, re.IGNORECASE) for pattern in step_patterns)
    
    def _detect_language(self, filename: str) -> Optional[str]:
        """Detect programming language from file extension"""
        lang_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".java": "Java",
            ".rb": "Ruby",
            ".ts": "TypeScript",
            ".go": "Go",
            ".cs": "C#",
        }
        
        for ext, lang in lang_map.items():
            if filename.endswith(ext):
                return lang
        
        return None
    
    def _format_commit_info(self, commit: Commit) -> Dict:
        """Format commit information"""
        return {
            "hash": commit.hash[:8],
            "author": commit.author.name,
            "date": commit.committer_date.isoformat(),
            "message": commit.msg.split('\n')[0][:100],
        }
    
    def _export_results(self) -> None:
        """Export mining results to CSV and JSON"""
        
        print(f"\n{'='*80}")
        print(f"📊 Mining Results")
        print(f"{'='*80}")
        
        # Summary stats
        print(f"\n📈 STATISTICS:")
        print(f"   Total repositories mined:        {self.stats['total_repositories']}")
        print(f"   Total commits analyzed:          {self.stats['total_commits_analyzed']}")
        print(f"   Commits with feature changes:    {self.stats['total_commits_with_features']}")
        print(f"   Total feature files found:       {self.stats['total_feature_files_found']}")
        print(f"   Total scenarios extracted:       {self.stats['total_scenarios_extracted']}")
        
        # Export main features CSV
        if self.features_extracted:
            csv_path = self.output_dir / f"{self.output_prefix}_features.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=self.features_extracted[0].keys()
                )
                writer.writeheader()
                writer.writerows(self.features_extracted)
            print(f"\n✓ Exported features to: {csv_path}")
        
        # Export detailed repository data JSON
        if self.repositories_mined:
            json_path = self.output_dir / f"{self.output_prefix}_repositories.json"
            
            # Convert sets to lists for JSON serialization
            repos_for_json = []
            for repo in self.repositories_mined:
                repo_copy = repo.copy()
                if isinstance(repo_copy.get("languages_in_steps"), set):
                    repo_copy["languages_in_steps"] = list(repo_copy["languages_in_steps"])
                repos_for_json.append(repo_copy)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(repos_for_json, f, indent=2, default=str)
            print(f"✓ Exported repository data to: {json_path}")
        
        # Export summary report
        summary_path = self.output_dir / f"{self.output_prefix}_summary.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("PyDriller BDD Feature Mining Report\n")
            f.write("="*80 + "\n\n")
            
            for repo in self.repositories_mined:
                f.write(f"Repository: {repo['repo_name']}\n")
                f.write(f"URL: {repo['repo_url']}\n")
                f.write(f"Branch: {repo['branch']}\n")
                f.write(f"Commits analyzed: {repo['commits_analyzed']}\n")
                f.write(f"Commits with features: {repo['commits_with_features']}\n")
                f.write(f"Feature files: {len(repo['feature_files'])}\n")
                f.write(f"Scenarios: {repo['total_scenarios']}\n")
                f.write(f"Languages: {', '.join(repo['languages_in_steps'])}\n")
                f.write(f"First commit: {repo['first_commit']['date'] if repo['first_commit'] else 'N/A'}\n")
                f.write(f"Last commit: {repo['last_commit']['date'] if repo['last_commit'] else 'N/A'}\n")
                
                if repo['feature_files']:
                    f.write(f"\nFeature Files:\n")
                    for feature in repo['feature_files']:
                        f.write(f"  - {feature['file_path']}\n")
                        f.write(f"    Scenarios: {feature['scenario_count']}\n")
                        f.write(f"    Modified in {feature['commits_count']} commits\n")
                        f.write(f"    By {len(feature['authors'])} authors\n")
                
                f.write("\n" + "-"*80 + "\n\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("OVERALL STATISTICS\n")
            f.write("="*80 + "\n")
            for key, value in self.stats.items():
                f.write(f"{key}: {value}\n")
        
        print(f"✓ Exported summary to: {summary_path}")
        print(f"\n{'='*80}\n")


if __name__ == "__main__":
    # Example repositories to mine
    REPOSITORIES_TO_MINE = [
        {
            "url": "https://github.com/cucumber/cucumber-js",
            "name": "cucumber-js",
            "branch": "main"
        },
        {
            "url": "https://github.com/cucumber/cucumber-python",
            "name": "cucumber-python",
            "branch": "main"
        },
        {
            "url": "https://github.com/cucumber/cucumber-jvm",
            "name": "cucumber-jvm",
            "branch": "main"
        },
    ]
    
    # Create miner and run
    miner = PyDrillerFeatureMiner(output_prefix="pydriller_bdd")
    miner.mine_multiple_repositories(REPOSITORIES_TO_MINE)
