#!/usr/bin/env python3
"""
Enhanced Feature File Evolution Analyzer

Tracks how .feature files evolve over time with multiple input modes:
- GitHub repository URLs
- Local cloned repository paths
- CSV files with metadata

Features:
- Multiple input modes (GitHub, local, CSV)
- Single unified progress bar
- Comprehensive logging
- Error handling & API failure recovery
- Execution summary & statistics

Usage:
    python3 enhanced_feature_evolution_analyzer.py
"""

import argparse
import os
import re
import json
import csv
import sys
import logging
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

from git import Repo
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class EnhancedFeatureEvolutionAnalyzer:
    """Enhanced analyzer with multiple input modes and comprehensive logging."""
    
    def __init__(self, output_base_dir: str = "evolution_analysis_results"):
        """Initialize the analyzer."""
        self.output_base = Path(output_base_dir)
        self.output_base.mkdir(exist_ok=True)
        
        # Logger and tracking (will be set per-repo)
        self.logger = logging.getLogger(__name__)
        self.current_repo_logger = None
        self.current_log_file = None
        
        # Statistics tracking
        self.stats = {
            'total_repositories': 0,
            'successful_analysis': 0,
            'failed_analysis': 0,
            'total_commits': 0,
            'total_feature_files': 0,
            'total_lines': 0,
            'start_time': datetime.now(),
            'repositories': [],
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Configure console-only logging."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Console handler only (file handlers added per-repo)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        ch.setFormatter(formatter)
        
        logger.addHandler(ch)
        return logger
    
    def _setup_repo_logging(self, log_file: Path) -> logging.Logger:
        """Configure logging for a specific repository (file + console)."""
        logger = logging.getLogger(f"repo_{log_file.stem}")
        logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def _parse_repo_url(self, url: str) -> Tuple[str, str]:
        """Extract owner and repo name from various URL formats."""
        url = url.strip()
        url = url.rstrip('/')
        if url.endswith('.git'):
            url = url[:-4]
        
        # Handle SSH format: git@github.com:owner/repo
        ssh_match = re.search(r"git@github\.com:([^/]+)/(.+)$", url)
        if ssh_match:
            return ssh_match.group(1), ssh_match.group(2)
        
        # If it's owner/repo format
        if "/" in url and not url.startswith("http"):
            parts = url.split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        # If it's a GitHub URL
        match = re.search(r"github\.com/([^/]+)/([^/?#]+)", url)
        if match:
            return match.group(1), match.group(2)
        
        raise ValueError(f"Invalid GitHub URL format: '{url}'")
    
    def _get_input_mode(self) -> Tuple[str, str]:
        """Display menu and get user's choice of input mode."""
        print("\n" + "="*70)
        print("🔍 Feature File Evolution Analyzer - Enhanced Version")
        print("="*70)
        print("\nSelect input mode:\n")
        print("1. GitHub Repository URL(s)")
        print("   → Provide one or more GitHub links")
        print("   → Clones and analyzes directly from GitHub\n")
        print("2. Local Repository Path(s)")
        print("   → Already cloned repositories on your system")
        print("   → Analyzes git history locally\n")
        print("3. CSV File with Metadata")
        print("   → Batch process multiple repos from CSV")
        print("   → Requires 'url' column in CSV\n")
        
        while True:
            choice = input("Enter your choice (1/2/3): ").strip()
            if choice in ['1', '2', '3']:
                modes = {'1': 'github', '2': 'local', '3': 'csv'}
                mode = modes[choice]
                self.logger.info(f"Selected input mode: {mode}")
                break
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
        
        return mode, self._get_input_for_mode(mode)
    
    def _get_file_tracking_mode(self) -> str:
        """Display menu and get user's choice of file tracking mode."""
        print("\n" + "="*70)
        print("📂 File Tracking Mode Selection")
        print("="*70)
        print("\nChoose what to analyze:\n")
        print("1. 🎯 Only .feature files")
        print("   → Analyze ONLY commits that modified .feature files")
        print("   → Skip commits with no .feature file changes")
        print("   → Focus on BDD specifications")
        print("   → FASTER processing (skips unrelated commits)\n")
        print("2. 📁 ALL file types")
        print("   → Track every file in the repository")
        print("   → Complete repository context")
        print("   → Includes .feature, .java, .yml, .md, etc.")
        print("   → More comprehensive but slower\n")
        
        while True:
            choice = input("Enter your choice (1/2): ").strip()
            if choice == '1':
                self.logger.info("Selected file tracking mode: feature_only")
                return 'feature_only'
            elif choice == '2':
                self.logger.info("Selected file tracking mode: all_files")
                return 'all_files'
            print("❌ Invalid choice. Please enter 1 or 2.")
    
    def _get_input_for_mode(self, mode: str) -> str:
        """Get specific input based on selected mode."""
        print("\n" + "-"*70)
        
        if mode == 'github':
            print("Enter GitHub repository URL(s):")
            print("Formats: owner/repo, https://github.com/owner/repo, etc.")
            print("For multiple repos, separate with commas")
            user_input = input("👉 Enter URL(s): ").strip()
            
            if not user_input:
                self.logger.error("No input provided")
                raise ValueError("GitHub URL cannot be empty")
            
            self.logger.info(f"GitHub input received: {len(user_input.split(','))} repo(s)")
            return user_input
        
        elif mode == 'local':
            print("Enter local repository path(s):")
            print("For multiple paths, separate with commas")
            user_input = input("👉 Enter path(s): ").strip()
            
            if not user_input:
                self.logger.error("No input provided")
                raise ValueError("Local path cannot be empty")
            
            # Validate paths exist
            paths = [p.strip() for p in user_input.split(',')]
            for path in paths:
                if not Path(path).exists():
                    self.logger.error(f"Path does not exist: {path}")
                    raise ValueError(f"Path does not exist: {path}")
            
            self.logger.info(f"Local paths input received: {len(paths)} repo(s)")
            return user_input
        
        elif mode == 'csv':
            csv_file = input("👉 Enter CSV file path: ").strip()
            csv_path = Path(csv_file)
            
            if not csv_path.exists():
                self.logger.error(f"CSV file not found: {csv_file}")
                raise FileNotFoundError(f"CSV file not found: {csv_file}")
            
            # Validate CSV has 'url' column
            try:
                df = pd.read_csv(csv_path)
                if 'url' not in df.columns:
                    self.logger.error("CSV missing 'url' column")
                    raise ValueError("CSV must have 'url' column")
                
                repo_count = len(df)
                self.logger.info(f"CSV loaded successfully: {repo_count} repositories")
                return csv_file
            except Exception as e:
                self.logger.error(f"Error reading CSV: {e}")
                raise
    
    def _parse_repositories(self, mode: str, user_input: str) -> List[Dict]:
        """Parse and validate repositories based on input mode."""
        repositories = []
        
        try:
            if mode == 'github':
                repos = [r.strip() for r in user_input.split(',')]
                for repo in repos:
                    try:
                        owner, repo_name = self._parse_repo_url(repo)
                        repositories.append({
                            'type': 'github',
                            'url': repo,
                            'owner': owner,
                            'repo_name': repo_name,
                        })
                        self.logger.debug(f"Parsed GitHub repo: {owner}/{repo_name}")
                    except Exception as e:
                        self.logger.error(f"Failed to parse GitHub URL '{repo}': {e}")
                        raise
            
            elif mode == 'local':
                paths = [p.strip() for p in user_input.split(',')]
                for path in paths:
                    repo_path = Path(path)
                    if not (repo_path / '.git').exists():
                        self.logger.error(f"Not a git repository: {path}")
                        raise ValueError(f"Not a git repository: {path}")
                    
                    repo_name = repo_path.name
                    repositories.append({
                        'type': 'local',
                        'path': str(repo_path.resolve()),
                        'repo_name': repo_name,
                    })
                    self.logger.debug(f"Parsed local repo: {repo_name} at {repo_path}")
            
            elif mode == 'csv':
                df = pd.read_csv(user_input)
                for idx, row in df.iterrows():
                    url = row['url']
                    try:
                        owner, repo_name = self._parse_repo_url(url)
                        repositories.append({
                            'type': 'github',
                            'url': url,
                            'owner': owner,
                            'repo_name': repo_name,
                            'metadata': row.to_dict(),
                        })
                        self.logger.debug(f"CSV entry {idx+1}: {owner}/{repo_name}")
                    except Exception as e:
                        self.logger.warning(f"Skipped invalid URL in CSV row {idx+1}: {url} - {e}")
            
            self.logger.info(f"Parsed {len(repositories)} repositories")
            return repositories
        
        except Exception as e:
            self.logger.error(f"Error parsing repositories: {e}")
            raise
    
    def analyze_repository(self, repo_info: Dict) -> bool:
        """Analyze a single repository."""
        repo_name = repo_info.get('repo_name', 'unknown')
        output_dir = None
        created_files = []
        
        try:
            # Create full repo identifier (owner/repo for GitHub, just name for local)
            if repo_info['type'] == 'github':
                owner = repo_info.get('owner', 'unknown')
                full_repo_id = f"{owner}_{repo_name}"  # Use _ instead of / for folder name
            else:
                full_repo_id = repo_name
            
            # Create output directory directly under output_base (no session folder)
            output_dir = self.output_base / full_repo_id
            output_dir.mkdir(exist_ok=True, parents=True)
            
            # Setup per-repo logging
            log_file = output_dir / f"evolution_analysis_{full_repo_id}.log"
            self.current_repo_logger = self._setup_repo_logging(log_file)
            created_files.append(str(log_file))
            
            self.current_repo_logger.info(f"Starting analysis: {full_repo_id}")
            
            # Handle different repository types
            if repo_info['type'] == 'github':
                repo = self._clone_github_repo(repo_info, output_dir)
            elif repo_info['type'] == 'local':
                repo = Repo(repo_info['path'])
            
            # Analyze evolution
            evolution_data = self._analyze_commits(repo, output_dir)
            
            # Generate outputs (pass full_repo_id for clean file naming)
            report_files = self._generate_reports(evolution_data, full_repo_id, output_dir)
            created_files.extend(report_files)
            
            self.current_repo_logger.info(f"✅ Successfully analyzed: {repo_name}")
            
            # Store statistics
            repo_stats = {
                'repo_name': repo_name,
                'full_repo_id': full_repo_id,
                'status': 'success',
                'commits': len(evolution_data),
                'output_dir': str(output_dir),
                'created_files': created_files,
                'error': None,
            }
            self.stats['repositories'].append(repo_stats)
            self.stats['successful_analysis'] += 1
            
            return True
        
        except Exception as e:
            error_msg = str(e)
            if self.current_repo_logger:
                self.current_repo_logger.error(f"❌ Failed to analyze {repo_name}: {error_msg}")
            else:
                print(f"❌ Error analyzing {repo_name}: {error_msg}")
            
            self.stats['repositories'].append({
                'repo_name': repo_name,
                'full_repo_id': repo_name,
                'status': 'failed',
                'commits': 0,
                'output_dir': str(output_dir) if output_dir else 'N/A',
                'created_files': created_files,
                'error': error_msg,
            })
            self.stats['failed_analysis'] += 1
            return False
    
    def _clone_github_repo(self, repo_info: Dict, output_dir: Path) -> Repo:
        """Clone GitHub repository with error handling."""
        try:
            https_url = f"https://github.com/{repo_info['owner']}/{repo_info['repo_name']}.git"
            clone_path = output_dir / "repo_clone"
            
            self.current_repo_logger.debug(f"Cloning from: {https_url}")
            repo = Repo.clone_from(https_url, str(clone_path), progress=None)
            
            self.current_repo_logger.debug("Repository cloned successfully")
            return repo
        
        except Exception as e:
            error_msg = str(e)
            if "Repository not found" in error_msg or "not found" in error_msg.lower():
                self.current_repo_logger.error(f"Repository not found: {https_url}")
                raise ValueError(f"Repository not found: {https_url}")
            elif "Connection" in error_msg or "timeout" in error_msg.lower():
                self.current_repo_logger.error(f"Connection error while cloning: {error_msg}")
                raise ConnectionError(f"Failed to connect to GitHub: {error_msg}")
            else:
                self.current_repo_logger.error(f"Clone failed: {error_msg}")
                raise
    
    def _analyze_commits(self, repo: Repo, output_dir: Path) -> List[Dict]:
        """Analyze all commits in repository."""
        try:
            commits = list(reversed(list(repo.iter_commits())))
            evolution_data = []
            
            self.current_repo_logger.info(f"Processing {len(commits)} commits")
            
            with tqdm(total=len(commits), desc="Analyzing commits", unit="commit") as pbar:
                for commit in commits:
                    try:
                        # Get feature files at this commit
                        feature_files = []
                        total_lines = 0
                        
                        for item in commit.tree.traverse():
                            if item.path.endswith(".feature"):
                                feature_files.append(item.path)
                                try:
                                    blob = commit.tree / item.path
                                    content = blob.data_stream.read().decode('utf-8', errors='ignore')
                                    total_lines += len(content.splitlines())
                                except:
                                    pass
                        
                        entry = {
                            'commit_hash': commit.hexsha[:7],
                            'timestamp': datetime.fromtimestamp(commit.committed_date),
                            'author': commit.author.name,
                            'feature_files_count': len(feature_files),
                            'total_lines': total_lines,
                            'files': feature_files,
                        }
                        
                        evolution_data.append(entry)
                        pbar.update(1)
                    
                    except Exception as e:
                        self.current_repo_logger.debug(f"Error processing commit {commit.hexsha[:7]}: {e}")
                        pbar.update(1)
            
            self.logger.info(f"Analyzed {len(evolution_data)} commits successfully")
            return evolution_data
        
        except Exception as e:
            self.current_repo_logger.error(f"Error analyzing commits: {e}")
            raise
    
    def _generate_reports(self, evolution_data: List[Dict], repo_id: str, output_dir: Path):
        """Generate CSV, JSON, and visualization reports."""
        try:
            self.logger.debug("Generating reports...")
            
            # CSV Timeline - use repo_id for filename
            df = pd.DataFrame([
                {
                    'Commit': e['commit_hash'],
                    'Date': e['timestamp'],
                    'Author': e['author'],
                    'Feature Files': e['feature_files_count'],
                    'Total Lines': e['total_lines'],
                }
                for e in evolution_data
            ])
            
            csv_file = output_dir / f"{repo_id}.csv"
            df.to_csv(csv_file, index=False)
            self.logger.debug(f"CSV report saved: {csv_file.name}")
            
            # JSON Statistics - use repo_id for filename
            stats = {
                'repository': repo_id,
                'total_commits': len(evolution_data),
                'feature_files_created': len(set(f for e in evolution_data for f in e['files'])),
                'feature_files_current': evolution_data[-1]['feature_files_count'] if evolution_data else 0,
                'total_lines_current': evolution_data[-1]['total_lines'] if evolution_data else 0,
                'average_growth': (evolution_data[-1]['total_lines'] - evolution_data[0]['total_lines']) / len(evolution_data) if len(evolution_data) > 1 else 0,
            }
            
            json_file = output_dir / f"{repo_id}.json"
            with open(json_file, 'w') as f:
                json.dump(stats, f, indent=2, default=str)
            self.logger.debug(f"JSON stats saved: {json_file.name}")
            
            # Visualization
            if len(evolution_data) > 0:
                self._create_visualization(evolution_data, repo_id, output_dir)
            
        except Exception as e:
            self.logger.error(f"Error generating reports: {e}")
            raise
    
    def _create_visualization(self, evolution_data: List[Dict], repo_id: str, output_dir: Path) -> Optional[str]:
        """Create visualization charts. Returns path to created PNG file."""
        try:
            self.current_repo_logger.debug("Creating visualization...")
            
            timestamps = [e['timestamp'] for e in evolution_data]
            feature_counts = [e['feature_files_count'] for e in evolution_data]
            total_lines = [e['total_lines'] for e in evolution_data]
            
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle(f"Feature Evolution: {repo_id}", fontsize=14, fontweight='bold')
            
            # Feature files over time
            axes[0, 0].plot(timestamps, feature_counts, marker='o', color='#4C9BE8')
            axes[0, 0].fill_between(timestamps, feature_counts, alpha=0.3, color='#4C9BE8')
            axes[0, 0].set_title("Feature Files Over Time")
            axes[0, 0].set_ylabel("Count")
            axes[0, 0].grid(True, alpha=0.3)
            
            # Lines of code over time
            axes[0, 1].plot(timestamps, total_lines, marker='s', color='#63C6A0')
            axes[0, 1].fill_between(timestamps, total_lines, alpha=0.3, color='#63C6A0')
            axes[0, 1].set_title("Total Lines Over Time")
            axes[0, 1].set_ylabel("Lines")
            axes[0, 1].grid(True, alpha=0.3)
            
            # Growth rate
            if len(evolution_data) > 1:
                window = max(1, len(evolution_data) // 10)
                moving_avg = pd.Series(total_lines).rolling(window=window).mean()
                axes[1, 0].plot(timestamps, moving_avg, color='#F5A623', linewidth=2)
                axes[1, 0].scatter(timestamps, total_lines, alpha=0.3, color='#F5A623')
                axes[1, 0].set_title("Growth Rate (Moving Average)")
                axes[1, 0].set_ylabel("Lines")
                axes[1, 0].grid(True, alpha=0.3)
            
            # Statistics box
            axes[1, 1].axis('off')
            stats_text = f"""
STATISTICS

Repository: {repo_id}
Commits: {len(evolution_data)}

Feature Files:
  Created: {len(set(f for e in evolution_data for f in e['files']))}
  Current: {feature_counts[-1] if feature_counts else 0}

Lines of Code:
  Current: {total_lines[-1] if total_lines else 0}
  Started: {total_lines[0] if total_lines else 0}
            """
            
            axes[1, 1].text(0.1, 0.5, stats_text, fontsize=10, verticalalignment='center',
                          fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            plt.tight_layout()
            
            png_file = output_dir / f"{repo_id}.png"
            plt.savefig(png_file, dpi=100, bbox_inches='tight')
            plt.close()
            
            self.current_repo_logger.debug(f"Visualization saved: {png_file.name}")
            return str(png_file)
        
        except Exception as e:
            self.current_repo_logger.warning(f"Error creating visualization: {e}")
            return None
    
    def run_batch_analysis(self, repositories: List[Dict]) -> bool:
        """Run analysis on multiple repositories."""
        try:
            self.stats['total_repositories'] = len(repositories)
            print(f"\n✅ Starting batch analysis for {len(repositories)} repository(ies)...")
            
            for i, repo in enumerate(repositories, 1):
                print(f"\n[{i}/{len(repositories)}] Analyzing {repo.get('repo_name', 'unknown')}...")
                self.analyze_repository(repo)
            
            return True
        
        except Exception as e:
            print(f"❌ Batch analysis error: {e}")
            return False
    
    def print_summary(self):
        """Print final execution summary with detailed file listings."""
        self.stats['end_time'] = datetime.now()
        duration = self.stats['end_time'] - self.stats['start_time']
        
        print("\n" + "="*80)
        print("📊 EXECUTION SUMMARY")
        print("="*80)
        
        print(f"\n📁 Output Directory: {self.output_base}")
        print(f"📈 Repositories Analyzed:")
        print(f"   • Total: {self.stats['total_repositories']}")
        print(f"   • Successful: {self.stats['successful_analysis']}")
        print(f"   • Failed: {self.stats['failed_analysis']}\n")
        
        success_rate = (self.stats['successful_analysis'] / self.stats['total_repositories'] * 100) if self.stats['total_repositories'] > 0 else 0
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"⏱️  Duration: {duration}\n")
        
        if self.stats['repositories']:
            print("="*80)
            print("📋 REPOSITORY DETAILS")
            print("="*80)
            
            for idx, repo in enumerate(self.stats['repositories'], 1):
                print(f"\n[{idx}] {repo['full_repo_id']}")
                print(f"    Status: {'✅ SUCCESS' if repo['status'] == 'success' else '❌ FAILED'}")
                
                if repo['status'] == 'success':
                    print(f"    Commits Analyzed: {repo['commits']}")
                    print(f"    Output Directory: {repo['output_dir']}")
                    print(f"    Files Created:")
                    if repo.get('created_files'):
                        for file_path in repo['created_files']:
                            file_obj = Path(file_path)
                            print(f"      • {file_obj.name}")
                    else:
                        print(f"      (No files created)")
                else:
                    print(f"    Error: {repo.get('error', 'Unknown error')}")
                    if repo.get('created_files'):
                        print(f"    Partial Output:")
                        for file_path in repo['created_files']:
                            file_obj = Path(file_path)
                            print(f"      • {file_obj.name}")
        
        print("\n" + "="*80)
        if self.stats['failed_analysis'] > 0:
            print(f"⚠️  {self.stats['failed_analysis']} repository(ies) failed.")
            print("Check the .log files in each repository folder for error details.")
        else:
            print("✅ All repositories analyzed successfully!")
        print("="*80 + "\n")


def main():
    """Main entry point."""
    try:
        analyzer = EnhancedFeatureEvolutionAnalyzer()
        logger = analyzer._setup_logging()
        
        # Get input mode and user input
        mode, user_input = analyzer._get_input_mode()
        
        # Get file tracking mode
        analyzer.file_tracking_mode = analyzer._get_file_tracking_mode()
        
        # Parse repositories
        repositories = analyzer._parse_repositories(mode, user_input)
        
        if not repositories:
            print("❌ No repositories to analyze")
            analyzer.logger.error("No repositories parsed")
            return 1
        
        print(f"\n✅ Ready to analyze {len(repositories)} repository(ies)\n")
        
        # Run batch analysis
        analyzer.run_batch_analysis(repositories)
        
        # Print summary
        analyzer.print_summary()
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
