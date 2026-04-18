#!/usr/bin/env python3
"""
Enhanced Feature File Evolution Analyzer - v2 with Comprehensive Error Handling

Tracks how .feature files evolve over time with multiple input modes:
- GitHub repository URLs
- Local cloned repository paths  
- CSV files with metadata

Features:
- Multiple input modes (GitHub, local, CSV)
- Single unified progress bar
- Comprehensive logging with DEBUG capabilities
- Error handling & API failure recovery with retry logic
- Execution summary & statistics
- System diagnostics and pre-flight validation checks
- Context-rich error messages for troubleshooting
- Stack trace capture for debugging
- Network connectivity validation

Usage:
    python3 enhanced_feature_evolution_analyzer_v2.py
"""

import argparse
import os
import re
import json
import csv
import sys
import logging
import shutil
import traceback
import platform
import socket
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from time import sleep

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError  
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# CUSTOM EXCEPTION CLASSES
# =============================================================================

class AnalyzerError(Exception):
    """Base exception for all analyzer errors."""
    pass


class RepositoryError(AnalyzerError):
    """Errors related to repository access, cloning, or validation."""
    pass


class GitOperationError(AnalyzerError):
    """Errors during git operations."""
    pass


class NetworkError(AnalyzerError):
    """Network and connectivity errors."""
    pass


class ValidationError(AnalyzerError):
    """Input validation errors."""
    pass


class FileOperationError(AnalyzerError):
    """File I/O and directory errors."""
    pass


# =============================================================================
# DIAGNOSTICS AND VALIDATION
# =============================================================================

class SystemDiagnostics:
    """System diagnostics for troubleshooting."""
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Gather system information."""
        try:
            return {
                'platform': platform.system(),
                'platform_release': platform.release(),
                'python_version': platform.python_version(),
                'git_available': shutil.which('git') is not None,
            }
        except Exception as e:
            return {'error': f'Failed to gather system info: {e}'}
    
    @staticmethod
    def check_network_connectivity(timeout: int = 5) -> Tuple[bool, str]:
        """Check network connectivity."""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            return True, "Network OK"
        except (socket.timeout, socket.error) as e:
            return False, f"No connectivity: {e}"
    
    @staticmethod
    def check_github_api(timeout: int = 5) -> Tuple[bool, str]:
        """Check GitHub API availability."""
        try:
            req = urllib.request.Request('https://api.github.com', method='HEAD')
            urllib.request.urlopen(req, timeout=timeout)
            return True, "GitHub API reachable"
        except urllib.error.URLError as e:
            return False, f"GitHub unreachable: {e}"
        except Exception as e:
            return False, f"Check failed: {e}"
    
    @staticmethod
    def check_local_permissions(path: Path) -> Tuple[bool, str]:
        """Check directory permissions."""
        try:
            if not path.exists():
                return False, f"Path does not exist: {path}"
            if not os.access(path, os.R_OK):
                return False, f"No read permission: {path}"
            if not os.access(path, os.W_OK):
                return False, f"No write permission: {path}"
            return True, f"Permissions OK"
        except Exception as e:
            return False, f"Check failed: {e}"


# =============================================================================
# MAIN ANALYZER CLASS
# =============================================================================

class EnhancedFeatureEvolutionAnalyzer:
    """Enhanced analyzer with comprehensive error handling and diagnostics."""
    
    def __init__(self, output_base_dir: str = "evolution_analysis_results"):
        """Initialize analyzer with diagnostics."""
        self.output_base = Path(output_base_dir)
        
        try:
            self.output_base.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            raise FileOperationError(
                f"Failed to create output directory: {e}\n"
                f"  Suggestion: Check disk space and permissions"
            )
        
        self.logger = logging.getLogger(__name__)
        self.current_repo_logger = None
        self.file_tracking_mode = None
        
        # Retry settings
        self.max_retries = 3
        self.retry_delay = 2
        
        # Statistics
        self.stats = {
            'total_repositories': 0,
            'successful_analysis': 0,
            'failed_analysis': 0,
            'total_commits': 0,
            'start_time': datetime.now(),
            'repositories': [],
        }
        
        # Run diagnostics
        self._run_diagnostics()
    
    def _run_diagnostics(self):
        """Run pre-flight system diagnostics."""
        diagnostics = SystemDiagnostics()
        self.diagnostics = {
            'system_info': diagnostics.get_system_info(),
            'network_ok': diagnostics.check_network_connectivity()[0],
            'github_ok': diagnostics.check_github_api()[0],
            'local_perms_ok': diagnostics.check_local_permissions(self.output_base)[0],
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Configure console logging."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # Log diagnostics
        logger.debug("PRE-FLIGHT DIAGNOSTICS:")
        logger.debug(f"  Platform: {self.diagnostics['system_info'].get('platform')}")
        logger.debug(f"  Network: {'✓' if self.diagnostics['network_ok'] else '✗'}")
        logger.debug(f"  GitHub API: {'✓' if self.diagnostics['github_ok'] else '✗'}")
        
        return logger
    
    def _setup_repo_logging(self, log_file: Path) -> logging.Logger:
        """Configure per-repository logging."""
        logger = logging.getLogger(f"repo_{log_file.stem}")
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        
        try:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(fh)
        except Exception as e:
            logger.warning(f"Could not create log file: {e}")
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(ch)
        
        return logger
    
    def _get_file_tracking_mode(self) -> str:
        """Get file tracking mode from user."""
        print("\n" + "="*70)
        print("🔍 Feature File Tracking Mode")
        print("="*70)
        print("\n1. Feature Files Only (*.feature)")
        print("   → More focused analysis")
        print("   → Faster processing\n")
        print("2. All Files")
        print("   → Complete repository context")
        print("   → Comprehensive analysis\n")
        
        while True:
            choice = input("Select mode (1/2): ").strip()
            if choice == '1':
                return 'feature_only'
            elif choice == '2':
                return 'all_files'
            print("❌ Invalid choice. Enter 1 or 2.")
    
    def _parse_repo_url(self, url: str) -> Tuple[str, str]:
        """Parse GitHub URL to owner and repo name."""
        url = url.strip()
        
        # Format: owner/repo
        if '/' in url and not url.startswith('http'):
            parts = url.split('/')
            if len(parts) >= 2:
                return parts[-2], parts[-1]
        
        # Format: https://github.com/owner/repo or https://github.com/owner/repo.git
        if 'github.com' in url:
            match = re.search(r'github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?/?$', url)
            if match:
                return match.group(1), match.group(2)
        
        raise ValidationError(f"Invalid GitHub URL format: '{url}'")
    
    def _get_input_mode(self) -> Tuple[str, str]:
        """Get input mode from user."""
        print("\n" + "="*70)
        print("🔍 Feature File Evolution Analyzer")
        print("="*70)
        print("\nSelect input mode:\n")
        print("1. GitHub Repository URL(s)")
        print("2. Local Repository Path(s)")
        print("3. CSV File with Metadata\n")
        
        while True:
            choice = input("Enter choice (1/2/3): ").strip()
            if choice in ['1', '2', '3']:
                modes = {'1': 'github', '2': 'local', '3': 'csv'}
                return modes[choice], self._get_input_for_mode(modes[choice])
            print("❌ Invalid. Enter 1, 2, or 3.")
    
    def _get_input_for_mode(self, mode: str) -> str:
        """Get input based on selected mode."""
        print("\n" + "-"*70)
        
        if mode == 'github':
            print("Enter GitHub repository URL(s):")
            print("Format: owner/repo or https://github.com/owner/repo")
            print("Multiple repos: comma-separated\n")
            user_input = input("👉 Enter URL(s): ").strip()
            if not user_input:
                raise ValidationError("GitHub URL cannot be empty")
            return user_input
        
        elif mode == 'local':
            print("Enter local repository path(s):")
            print("Multiple paths: comma-separated\n")
            user_input = input("👉 Enter path(s): ").strip()
            if not user_input:
                raise ValidationError("Path cannot be empty")
            return user_input
        
        elif mode == 'csv':
            print("Enter path to CSV file (must have 'url' column):\n")
            user_input = input("👉 Enter file path: ").strip()
            if not user_input:
                raise ValidationError("File path cannot be empty")
            return user_input
    
    def _parse_repositories(self, mode: str, user_input: str) -> List[Dict]:
        """Parse and validate repositories."""
        repositories = []
        
        try:
            self.logger.info(f"Parsing repositories in '{mode}' mode...")
            
            if mode == 'github':
                for idx, repo_url in enumerate([r.strip() for r in user_input.split(',')], 1):
                    if not repo_url:
                        continue
                    try:
                        owner, repo_name = self._parse_repo_url(repo_url)
                        repositories.append({
                            'type': 'github',
                            'url': repo_url,
                            'owner': owner,
                            'repo_name': repo_name,
                        })
                        self.logger.debug(f"[{idx}] Parsed: {owner}/{repo_name}")
                    except ValidationError as e:
                        raise RepositoryError(
                            f"Invalid GitHub URL: '{repo_url}'\n"
                            f"  {e}\n"
                            f"  Format: owner/repo or https://github.com/owner/repo"
                        )
            
            elif mode == 'local':
                for idx, path_str in enumerate([p.strip() for p in user_input.split(',')], 1):
                    if not path_str:
                        continue
                    try:
                        repo_path = Path(path_str).expanduser().resolve()
                        
                        if not repo_path.exists():
                            raise RepositoryError(f"Path does not exist: {path_str}")
                        if not repo_path.is_dir():
                            raise RepositoryError(f"Not a directory: {path_str}")
                        if not (repo_path / '.git').exists():
                            raise RepositoryError(f"Not a git repo: {path_str}")
                        if not os.access(repo_path, os.R_OK):
                            raise RepositoryError(f"No read permission: {path_str}")
                        
                        repositories.append({
                            'type': 'local',
                            'path': str(repo_path),
                            'repo_name': repo_path.name,
                        })
                        self.logger.debug(f"[{idx}] Validated: {repo_path.name}")
                    
                    except RepositoryError:
                        raise
            
            elif mode == 'csv':
                try:
                    df = pd.read_csv(user_input)
                except FileNotFoundError:
                    raise RepositoryError(f"CSV file not found: {user_input}")
                except Exception as e:
                    raise ValidationError(f"Failed to read CSV: {e}")
                
                if 'url' not in df.columns:
                    raise ValidationError(
                        f"CSV missing 'url' column. Have: {', '.join(df.columns)}"
                    )
                
                for idx, row in df.iterrows():
                    url = row.get('url', '').strip()
                    if not url:
                        self.logger.warning(f"Row {idx+1}: empty URL, skipping")
                        continue
                    try:
                        owner, repo_name = self._parse_repo_url(url)
                        repositories.append({
                            'type': 'github',
                            'url': url,
                            'owner': owner,
                            'repo_name': repo_name,
                            'metadata': row.to_dict(),
                        })
                    except ValidationError as e:
                        self.logger.warning(f"Row {idx+1}: invalid URL, skipping")
            
            if not repositories:
                raise ValidationError("No valid repositories found")
            
            self.logger.info(f"Parsed {len(repositories)} repositories")
            return repositories
        
        except (ValidationError, RepositoryError) as e:
            self.logger.error(f"Parse error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise AnalyzerError(f"Failed to parse repositories: {e}")
    
    def _clone_github_repo(self, repo_info: Dict, output_dir: Path) -> Repo:
        """Clone GitHub repository with retry logic."""
        owner = repo_info['owner']
        repo_name = repo_info['repo_name']
        url = f"https://github.com/{owner}/{repo_name}.git"
        clone_path = output_dir / "repo_clone"
        
        self.current_repo_logger.info(f"Cloning: {owner}/{repo_name}")
        self.current_repo_logger.debug(f"URL: {url}")
        
        for attempt in range(1, self.max_retries + 1):
            try:
                self.current_repo_logger.debug(f"Attempt {attempt}/{self.max_retries}")
                repo = Repo.clone_from(url, str(clone_path), progress=None)
                self.current_repo_logger.info("Clone successful")
                return repo
            
            except GitCommandError as e:
                error_msg = str(e)
                
                if "not found" in error_msg.lower() or "404" in error_msg:
                    raise RepositoryError(
                        f"Repository not found: {owner}/{repo_name}\n"
                        f"  Verify: owner/repo name, public access"
                    )
                
                if attempt < self.max_retries:
                    self.current_repo_logger.warning(
                        f"Connection error, retry in {self.retry_delay}s..."
                    )
                    sleep(self.retry_delay)
                    continue
                
                raise GitOperationError(f"Clone failed: {error_msg}")
            
            except Exception as e:
                if attempt < self.max_retries:
                    self.current_repo_logger.debug(f"Retry: {e}")
                    sleep(self.retry_delay)
                    continue
                raise
        
        raise GitOperationError(
            f"Failed after {self.max_retries} attempts: {owner}/{repo_name}"
        )
    
    def _unshallow_if_needed(self, repo: Repo, repo_path: str):
        """
        Detect and unshallow a shallow git clone.
        
        Shallow clones (created with --depth 1) only have the latest commit.
        This method detects shallow clones and converts them to full clones
        by fetching all missing commits from the remote.
        
        Args:
            repo: GitPython Repo object
            repo_path: Original repository path
        """
        try:
            shallow_file = Path(repo_path) / '.git' / 'shallow'
            
            if shallow_file.exists():
                self.current_repo_logger.info(
                    "🔍 Detected shallow clone (only latest commit). "
                    "Unshallowing to fetch full history..."
                )
                
                try:
                    # Unshallow the repository
                    repo.git.fetch('--unshallow')
                    self.current_repo_logger.info(
                        "✅ Repository unshallowed successfully. "
                        "Full commit history now available."
                    )
                except Exception as e:
                    # If unshallow fails, try regular fetch with --all
                    try:
                        self.current_repo_logger.warning(
                            f"Unshallow failed ({str(e)[:50]}...). "
                            "Attempting alternative fetch..."
                        )
                        repo.git.fetch('--all')
                        self.current_repo_logger.info(
                            "✅ Fetch completed. History may be incomplete."
                        )
                    except Exception as e2:
                        # If all else fails, log warning but proceed with shallow data
                        self.current_repo_logger.warning(
                            f"⚠️  Could not unshallow repository: {str(e2)[:100]}...\n"
                            f"Proceeding with shallow clone data (latest commit only). "
                            f"To fix manually: cd {repo_path} && git fetch --unshallow"
                        )
            else:
                self.current_repo_logger.debug("✓ Full clone detected (not shallow)")
        
        except Exception as e:
            # Non-fatal error, log and continue
            self.current_repo_logger.debug(f"Shallow check error: {e}")
    
    def _analyze_commits(self, repo: Repo, output_dir: Path) -> List[Dict]:
        """Analyze commits in repository."""
        try:
            self.current_repo_logger.info("Analyzing commits...")
            
            try:
                commits = list(reversed(list(repo.iter_commits())))
            except Exception as e:
                raise GitOperationError(f"Could not read commits: {e}")
            
            if not commits:
                self.current_repo_logger.warning("No commits found")
                return []
            
            self.current_repo_logger.info(f"Found {len(commits)} commits")
            
            evolution_data = []
            mode_desc = "feature only" if self.file_tracking_mode == 'feature_only' else "all files"
            
            skip_count = 0
            with tqdm(total=len(commits), desc="Commits", unit="") as pbar:
                for commit in commits:
                    try:
                        files = []
                        lines = 0
                        
                        for item in commit.tree.traverse():
                            if self.file_tracking_mode == 'feature_only':
                                if not item.path.endswith('.feature'):
                                    continue
                            
                            files.append(item.path)
                            try:
                                blob = commit.tree / item.path
                                content = blob.data_stream.read().decode('utf-8', errors='ignore')
                                lines += len(content.splitlines())
                            except:
                                pass
                        
                        if self.file_tracking_mode == 'feature_only' and not files:
                            skip_count += 1
                        else:
                            evolution_data.append({
                                'commit_hash': commit.hexsha[:7],
                                'timestamp': datetime.fromtimestamp(commit.committed_date),
                                'author': commit.author.name,
                                'feature_files_count': len([f for f in files if f.endswith('.feature')]),
                                'total_lines': lines,
                                'files': files,
                            })
                        
                        pbar.update(1)
                    
                    except Exception as e:
                        self.current_repo_logger.debug(f"Commit error: {e}")
                        pbar.update(1)
            
            self.current_repo_logger.info(f"Analyzed {len(evolution_data)} commits ({skip_count} skipped)")
            return evolution_data
        
        except GitOperationError:
            raise
        except Exception as e:
            self.current_repo_logger.error(f"Analysis failed: {e}")
            raise GitOperationError(f"Failed to analyze commits: {e}")
    
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
            axes[0, 0].plot(timestamps, feature_counts, marker='o', linewidth=2, markersize=4, color='#4C9BE8')
            axes[0, 0].fill_between(timestamps, feature_counts, alpha=0.3, color='#4C9BE8')
            axes[0, 0].set_title("Feature Files Count Over Time", fontweight='bold')
            axes[0, 0].set_xlabel("Date")
            axes[0, 0].set_ylabel("Number of .feature Files")
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Lines of code over time
            axes[0, 1].plot(timestamps, total_lines, marker='s', linewidth=2, markersize=4, color='#63C6A0')
            axes[0, 1].fill_between(timestamps, total_lines, alpha=0.3, color='#63C6A0')
            axes[0, 1].set_title("Total Lines of Code Over Time", fontweight='bold')
            axes[0, 1].set_xlabel("Date")
            axes[0, 1].set_ylabel("Total Lines")
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Growth rate
            if len(evolution_data) > 1:
                window = max(1, len(evolution_data) // 10)
                moving_avg = pd.Series(total_lines).rolling(window=window).mean()
                axes[1, 0].plot(timestamps, moving_avg, linewidth=2.5, color='#F5A623', label='Moving Average')
                axes[1, 0].scatter(timestamps, total_lines, alpha=0.3, s=20, color='#F5A623', label='Actual')
                axes[1, 0].set_title(f"Growth Rate (Moving Average, window={window})", fontweight='bold')
                axes[1, 0].set_xlabel("Date")
                axes[1, 0].set_ylabel("Lines of Code")
                axes[1, 0].legend()
                axes[1, 0].grid(True, alpha=0.3)
                axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Statistics box
            axes[1, 1].axis('off')
            
            # Calculate metrics
            num_commits = len(evolution_data)
            num_feature_files_created = len(set(f for e in evolution_data for f in e['files']))
            current_feature_files = feature_counts[-1] if feature_counts else 0
            initial_feature_files = feature_counts[0] if feature_counts else 0
            feature_files_growth = current_feature_files - initial_feature_files
            
            current_loc = total_lines[-1] if total_lines else 0
            initial_loc = total_lines[0] if total_lines else 0
            loc_growth = current_loc - initial_loc
            
            avg_growth = loc_growth / num_commits if num_commits > 0 else 0
            peak_loc = max(total_lines) if total_lines else 0
            lowest_loc = min(total_lines) if total_lines else 0
            
            stats_text = f"""
EVOLUTION STATISTICS

Repository: {repo_id}
Commits Analyzed: {num_commits:,}

Feature Files:
  • Created: {num_feature_files_created}
  • Current: {current_feature_files}
  • Growth: {feature_files_growth} files

Lines of Code:
  • Current: {current_loc:,} LOC
  • Started: {initial_loc:,} LOC
  • Growth: {loc_growth:+,} lines

Metrics:
  • Avg growth: {avg_growth:.1f} lines/commit
  • Peak: {peak_loc:,} lines
  • Lowest: {lowest_loc:,} lines
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

    def _generate_reports(self, evolution_data: List[Dict], repo_id: str, output_dir: Path) -> List[str]:
        """Generate reports (CSV, JSON, PNG)."""
        created_files = []
        
        try:
            self.current_repo_logger.info("Generating reports...")
            
            # CSV
            df = pd.DataFrame([
                {
                    'Commit': e['commit_hash'],
                    'Date': e['timestamp'],
                    'Author': e['author'],
                    'Feature Files': e['feature_files_count'],
                    'Lines': e['total_lines'],
                }
                for e in evolution_data
            ])
            
            csv_file = output_dir / f"{repo_id}.csv"
            df.to_csv(csv_file, index=False)
            created_files.append(str(csv_file))
            
            # JSON
            stats = {
                'repo': repo_id,
                'commits': len(evolution_data),
                'files': len(set(f for e in evolution_data for f in e['files'])),
            }
            json_file = output_dir / f"{repo_id}.json"
            json_file.write_text(json.dumps(stats, indent=2))
            created_files.append(str(json_file))
            
            # PNG Visualization
            if evolution_data:
                png_file = self._create_visualization(evolution_data, repo_id, output_dir)
                if png_file:
                    created_files.append(png_file)
            
            self.current_repo_logger.info(f"Generated {len(created_files)} reports")
            return created_files
        
        except Exception as e:
            self.current_repo_logger.warning(f"Report generation failed: {e}")
            return created_files
    
    def analyze_repository(self, repo_info: Dict) -> bool:
        """Analyze single repository."""
        repo_name = repo_info.get('repo_name', 'unknown')
        output_dir = None
        created_files = []
        
        try:
            # Setup
            if repo_info['type'] == 'github':
                full_repo_id = f"{repo_info.get('owner')}_{repo_name}"
            else:
                full_repo_id = repo_name
            
            output_dir = self.output_base / full_repo_id
            output_dir.mkdir(exist_ok=True, parents=True)
            
            log_file = output_dir / f"{full_repo_id}.log"
            self.current_repo_logger = self._setup_repo_logging(log_file)
            created_files.append(str(log_file))
            
            self.current_repo_logger.info(f"Analyzing: {full_repo_id}")
            
            # Clone/open repo
            if repo_info['type'] == 'github':
                repo = self._clone_github_repo(repo_info, output_dir)
            else:
                try:
                    repo = Repo(repo_info['path'])
                    # Handle shallow clones by unshallowing if needed
                    self._unshallow_if_needed(repo, repo_info['path'])
                except InvalidGitRepositoryError:
                    raise RepositoryError(f"Invalid git repo: {repo_info['path']}")
            
            # Analyze
            evolution_data = self._analyze_commits(repo, output_dir)
            
            # Generate reports
            reports = self._generate_reports(evolution_data, full_repo_id, output_dir)
            created_files.extend(reports)
            
            # Success
            print(f"  ✅ {repo_name}")
            self.stats['repositories'].append({
                'name': repo_name,
                'id': full_repo_id,
                'status': 'success',
                'commits': len(evolution_data),
                'output': str(output_dir),
                'files': created_files,
            })
            self.stats['successful_analysis'] += 1
            return True
        
        except (RepositoryError, GitOperationError) as e:
            print(f"  ❌ {repo_name}: {str(e)[:60]}...")
            self.stats['repositories'].append({
                'name': repo_name,
                'id': repo_name,
                'status': 'failed',
                'error': str(e),
            })
            self.stats['failed_analysis'] += 1
            return False
        
        except Exception as e:
            print(f"  ❌ {repo_name}: Unexpected error")
            if self.current_repo_logger:
                self.current_repo_logger.error(f"Unexpected: {e}")
                self.current_repo_logger.debug(traceback.format_exc())
            self.stats['failed_analysis'] += 1
            return False
    
    def run_batch_analysis(self, repositories: List[Dict]):
        """Run analysis on all repositories."""
        self.stats['total_repositories'] = len(repositories)
        print(f"\nAnalyzing {len(repositories)} repository(ies)...\n")
        self.logger.info(f"Starting batch analysis...")
        
        for i, repo in enumerate(repositories, 1):
            print(f"[{i}/{len(repositories)}] {repo.get('repo_name', '?')}")
            try:
                self.analyze_repository(repo)
            except KeyboardInterrupt:
                print("\n⚠️  Interrupted by user")
                raise
            except Exception as e:
                self.logger.error(f"Error: {e}")
    
    def print_summary(self):
        """Print execution summary."""
        self.stats['end_time'] = datetime.now()
        duration = self.stats['end_time'] - self.stats['start_time']
        
        print("\n" + "="*70)
        print("📊 SUMMARY")
        print("="*70)
        print(f"\nRepositories: {self.stats['successful_analysis']}/{self.stats['total_repositories']} successful")
        print(f"Duration: {duration}")
        print(f"Output: {self.output_base}\n")
        
        if self.stats['failed_analysis'] > 0:
            print(f"⚠️  {self.stats['failed_analysis']} failed - see .log files for details")
        else:
            print("✅ All analyses completed successfully!")
        print("="*70 + "\n")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point."""
    try:
        # Initialize
        analyzer = EnhancedFeatureEvolutionAnalyzer()
        logger = analyzer._setup_logging()
        
        # Get input
        mode, user_input = analyzer._get_input_mode()
        logger.info(f"Mode: {mode}")
        
        # Parse repositories
        repositories = analyzer._parse_repositories(mode, user_input)
        if not repositories:
            print("❌ No repositories found")
            return 1
        
        # Get file tracking mode
        analyzer.file_tracking_mode = analyzer._get_file_tracking_mode()
        logger.info(f"Tracking: {analyzer.file_tracking_mode}")
        
        # Analyze
        print(f"\n✅ Analyzing {len(repositories)} repo(ies)...\n")
        analyzer.run_batch_analysis(repositories)
        
        # Summary
        analyzer.print_summary()
        return 0
    
    except ValidationError as e:
        print(f"❌ Error: {e}")
        return 1
    except RepositoryError as e:
        print(f"❌ Repository Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
        return 130
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print(f"\nDebug info:")
        print(f"  {traceback.format_exc()}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
