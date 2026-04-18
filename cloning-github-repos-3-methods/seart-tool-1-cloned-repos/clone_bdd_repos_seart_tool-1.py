#!/usr/bin/env python3
"""
BDD Repository Cloner with Checkpoint Support
- Clones repositories with feature_count >= 10
- Tracks skipped repositories
- Checkpoint system for resuming interrupted runs
- Comprehensive logging and error handling
- Single progress bar for entire operation
"""

import os
import sys
import csv
import json
import logging
import shutil
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from tqdm import tqdm

# Configuration
CSV_FILE = None
MIN_FEATURE_COUNT = 10

# Dynamic configuration (will be set by user input)
CLONED_REPOS_DIR = None
CHECKPOINT_FILE = None
LOG_FILE = None
STATS_FILE = None

# Configure basic logging (will be reconfigured in main with file handler)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RepositoryCloner:
    """Manages BDD repository cloning with checkpoint support"""
    
    def __init__(self, csv_file: str, cloned_dir: str, checkpoint_file: str):
        self.csv_file = csv_file
        self.cloned_dir = cloned_dir
        self.checkpoint_file = checkpoint_file
        
        # Statistics
        self.stats = {
            'total_repos': 0,
            'processed': 0,
            'cloned': 0,
            'skipped': 0,
            'errors': 0,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'skipped_repos': [],
            'failed_repos': [],
            'cloned_repos': []
        }
        
        # Connection check
        self.connection_ok = False
        
    def check_connection(self) -> bool:
        """Verify internet connection to GitHub"""
        logger.info("🔍 Checking connection to GitHub...")
        try:
            socket.create_connection(("github.com", 443), timeout=5)
            logger.info("✅ Connection to GitHub established successfully")
            self.connection_ok = True
            return True
        except (socket.timeout, socket.error) as e:
            logger.error(f"❌ Failed to connect to GitHub: {e}")
            self.connection_ok = False
            return False
    
    def create_output_dir(self) -> bool:
        """Create output directory for cloned repos"""
        try:
            Path(self.cloned_dir).mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Created/verified output directory: {self.cloned_dir}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create output directory: {e}")
            return False
    
    def load_checkpoint(self) -> Dict:
        """Load checkpoint from previous run"""
        if not Path(self.checkpoint_file).exists():
            logger.info("📋 No previous checkpoint found, starting fresh")
            return {'processed_rows': []}
        
        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
            
            processed_rows = checkpoint.get('processed_rows', [])
            stats = checkpoint.get('statistics', {})
            
            # Enhanced resumption message
            if stats:
                logger.info(
                    f"📋 Checkpoint loaded - Resuming from: {len(processed_rows)} repos processed "
                    f"({stats.get('successfully_cloned', 0)} ✅, "
                    f"{stats.get('skipped', 0)} ⏭️, "
                    f"{stats.get('errors', 0)} ❌)"
                )
            else:
                logger.info(
                    f"📋 Checkpoint loaded - Resuming from: {len(processed_rows)} repos already processed"
                )
            
            return checkpoint
        except Exception as e:
            logger.error(f"⚠️  Failed to load checkpoint: {e}, starting fresh")
            return {'processed_rows': []}
    
    def save_checkpoint(self, processed_rows: List[int]):
        """Save current progress checkpoint with detailed state"""
        try:
            checkpoint = {
                'processed_rows': processed_rows,
                'statistics': {
                    'total_processed': self.stats['processed'],
                    'successfully_cloned': self.stats['cloned'],
                    'skipped': self.stats['skipped'],
                    'errors': self.stats['errors']
                },
                'timestamp': datetime.now().isoformat()
            }
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)
            logger.debug(f"💾 Checkpoint saved: {len(processed_rows)} rows processed "
                        f"({self.stats['cloned']} cloned, {self.stats['skipped']} skipped, {self.stats['errors']} errors)")
        except Exception as e:
            logger.error(f"⚠️  Failed to save checkpoint: {e}")
    
    def clone_repository(self, repo_url: str, repo_name: str) -> Tuple[bool, str]:
        """Clone a single repository"""
        try:
            target_dir = os.path.join(self.cloned_dir, repo_name)
            
            # Skip if already cloned
            if os.path.exists(target_dir):
                msg = f"Repository already cloned: {repo_name}"
                logger.info(f"⏭️  {msg}")
                return True, msg
            
            logger.debug(f"🔄 Cloning: {repo_url}")
            
            # Clone with timeout (full clone with complete history)
            result = subprocess.run(
                ['git', 'clone', repo_url, target_dir],
                capture_output=True,
                text=True,
                timeout=300  # Increased timeout for full clone (5 minutes)
            )
            
            if result.returncode == 0:
                msg = f"Successfully cloned: {repo_name}"
                logger.info(f"✅ {msg}")
                return True, msg
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                msg = f"Clone failed: {error_msg}"
                logger.warning(f"⚠️  {msg}")
                return False, msg
                
        except subprocess.TimeoutExpired:
            msg = f"Clone timeout (60s): {repo_name}"
            logger.error(f"❌ {msg}")
            return False, msg
        except Exception as e:
            msg = f"Clone error: {str(e)}"
            logger.error(f"❌ {msg}")
            return False, msg
    
    def validate_gherkin_content(self, repo_path: str) -> Tuple[bool, str]:
        """Validate that cloned repo contains actual Gherkin feature files with Given-When-Then keywords.
        
        Checks for Gherkin keywords in any case (given/Given/GIVEN, when/When/WHEN, etc.).
        A valid repository must have at least one .feature file containing proper Gherkin syntax.
        """
        try:
            repo_path_obj = Path(repo_path)
            
            # Find all .feature files
            feature_files = list(repo_path_obj.rglob("*.feature"))
            
            if not feature_files:
                return False, "No .feature files found"
            
            # Check if at least one feature file contains Gherkin keywords (case-insensitive)
            # Supports: given, Given, GIVEN, when, When, WHEN, etc.
            gherkin_keywords_upper = {'GIVEN', 'WHEN', 'THEN', 'AND', 'BUT'}
            gherkin_keywords_lower = {'given', 'when', 'then', 'and', 'but'}
            valid_files = 0
            invalid_reasons = []
            
            for feature_file in feature_files:
                try:
                    content = feature_file.read_text(encoding='utf-8', errors='ignore')
                    # Check for keywords in both uppercase and lowercase (case-insensitive)
                    content_upper = content.upper()
                    has_keywords = (any(kw in content_upper for kw in gherkin_keywords_upper) or 
                                  any(kw in content for kw in gherkin_keywords_lower))
                    
                    if has_keywords:
                        valid_files += 1
                except Exception as e:
                    invalid_reasons.append(f"{feature_file.name}: {str(e)}")
            
            if valid_files == 0:
                reason_detail = f" ({len(feature_files)} .feature file(s) found but none contain Given/When/Then keywords)"
                return False, f"No valid Gherkin content{reason_detail}"
            
            return True, f"✓ {valid_files}/{len(feature_files)} file(s) with valid Gherkin keywords"
        
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def read_csv_rows(self) -> List[Dict]:
        """Read all rows from CSV file"""
        try:
            rows = []
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            logger.info(f"📖 CSV file loaded: {len(rows)} total repositories")
            return rows
        except Exception as e:
            logger.error(f"❌ Failed to read CSV file: {e}")
            return []
    
    def run(self):
        """Main execution loop"""
        logger.info("=" * 70)
        logger.info("🚀 BDD Repository Cloner started")
        logger.info("=" * 70)
        
        # Pre-flight checks
        if not self.check_connection():
            logger.error("❌ Cannot proceed without internet connection")
            sys.exit(1)
        
        if not self.create_output_dir():
            logger.error("❌ Cannot proceed without output directory")
            sys.exit(1)
        
        # Load data
        rows = self.read_csv_rows()
        if not rows:
            logger.error("❌ No repositories to process")
            sys.exit(1)
        
        self.stats['total_repos'] = len(rows)
        
        # Load checkpoint
        checkpoint = self.load_checkpoint()
        processed_row_indices = set(checkpoint.get('processed_rows', []))
        
        # Process repositories
        processed_rows = list(processed_row_indices)
        
        logger.info(f"📊 Processing flow: Total={len(rows)}, Resume from={len(processed_rows)}")
        logger.info("=" * 70)
        
        with tqdm(total=len(rows), desc="Repository Processing", unit="repo") as pbar:
            for idx, row in enumerate(rows):
                try:
                    # Skip already processed rows
                    if idx in processed_row_indices:
                        pbar.update(1)
                        continue
                    
                    # Extract data
                    sno = row.get('sno', idx + 1)
                    github_url = row.get('github_url', '').strip()
                    feature_count_str = row.get('feature_count', '0').strip()
                    
                    # Parse feature count
                    try:
                        feature_count = int(feature_count_str)
                    except ValueError:
                        feature_count = 0
                    
                    # Determine action
                    if feature_count < MIN_FEATURE_COUNT:
                        self.stats['skipped'] += 1
                        self.stats['skipped_repos'].append({
                            'sno': sno,
                            'url': github_url,
                            'feature_count': feature_count,
                            'reason': 'feature_count < 10'
                        })
                        pbar.set_postfix({
                            'Cloned': self.stats['cloned'],
                            'Skipped': self.stats['skipped'],
                            'Errors': self.stats['errors']
                        })
                        pbar.update(1)
                    elif not github_url:
                        self.stats['skipped'] += 1
                        self.stats['skipped_repos'].append({
                            'sno': sno,
                            'url': 'N/A',
                            'feature_count': feature_count,
                            'reason': 'no_github_url'
                        })
                        pbar.set_postfix({
                            'Cloned': self.stats['cloned'],
                            'Skipped': self.stats['skipped'],
                            'Errors': self.stats['errors']
                        })
                        pbar.update(1)
                    else:
                        # Extract owner/repo from URL (e.g., thebrainfamily/cypress-cucumber-preprocessor)
                        url_parts = github_url.rstrip('/').replace('.git', '').split('/')
                        if len(url_parts) >= 2:
                            owner = url_parts[-2]
                            repo = url_parts[-1]
                            repo_name = f"{owner}/{repo}"
                        else:
                            repo_name = github_url.split('/')[-1].replace('.git', '')
                        
                        # Clone repository
                        success, message = self.clone_repository(github_url, repo_name)
                        
                        if success:
                            # Validate Gherkin content
                            target_dir = os.path.join(self.cloned_dir, repo_name)
                            is_valid, validation_msg = self.validate_gherkin_content(target_dir)
                            
                            if is_valid:
                                self.stats['cloned'] += 1
                                self.stats['cloned_repos'].append({
                                    'sno': sno,
                                    'url': github_url,
                                    'feature_count': feature_count,
                                    'repo_name': repo_name,
                                    'validation': validation_msg
                                })
                                logger.info(f"✅ Validated: {validation_msg}")
                            else:
                                # Remove invalid clone - ensure complete cleanup including empty parent dirs
                                try:
                                    if os.path.exists(target_dir):
                                        shutil.rmtree(target_dir, ignore_errors=False)
                                        logger.warning(f"⚠️  Removed invalid clone folder: {target_dir}")
                                        
                                        # Also remove empty parent directory (owner folder) if it's empty
                                        parent_dir = os.path.dirname(target_dir)
                                        if os.path.exists(parent_dir) and not os.listdir(parent_dir):
                                            try:
                                                os.rmdir(parent_dir)
                                                logger.info(f"🗑️  Cleaned up empty parent directory: {parent_dir}")
                                            except Exception:
                                                pass
                                    else:
                                        logger.warning(f"ℹ️  Folder already removed: {target_dir}")
                                except Exception as e:
                                    logger.error(f"❌ Failed to remove invalid clone folder '{target_dir}': {e}")
                                
                                self.stats['skipped'] += 1
                                self.stats['skipped_repos'].append({
                                    'sno': sno,
                                    'url': github_url,
                                    'feature_count': feature_count,
                                    'reason': f'invalid_gherkin_content: {validation_msg}',
                                    'repo_name': repo_name,
                                    'status': 'FAILED_VALIDATION'
                                })
                        else:
                            self.stats['errors'] += 1
                            self.stats['failed_repos'].append({
                                'sno': sno,
                                'url': github_url,
                                'feature_count': feature_count,
                                'error': message
                            })
                        
                        pbar.set_postfix({
                            'Cloned': self.stats['cloned'],
                            'Skipped': self.stats['skipped'],
                            'Errors': self.stats['errors']
                        })
                        pbar.update(1)
                    
                    # Update and save checkpoint every 5 repos
                    self.stats['processed'] += 1
                    processed_rows.append(idx)
                    if self.stats['processed'] % 5 == 0:
                        self.save_checkpoint(processed_rows)
                    
                except Exception as e:
                    logger.error(f"❌ Unexpected error processing row {idx}: {e}")
                    self.stats['errors'] += 1
                    self.stats['processed'] += 1
                    pbar.update(1)
                    processed_rows.append(idx)
        
        # Final checkpoint save
        self.save_checkpoint(processed_rows)
        
        # Generate statistics
        self.stats['end_time'] = datetime.now().isoformat()
        self.save_statistics()
        self.generate_results_csv()
        
        # Print summary
        logger.info("=" * 70)
        logger.info("📊 EXECUTION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Total Repositories: {self.stats['total_repos']}")
        logger.info(f"Processed: {self.stats['processed']}")
        logger.info(f"✅ Cloned: {self.stats['cloned']}")
        logger.info(f"⏭️  Skipped: {self.stats['skipped']}")
        logger.info(f"⚠️  Errors: {self.stats['errors']}")
        logger.info(f"📁 Clone Directory: {self.cloned_dir}")
        logger.info(f"📋 Checkpoint File: {self.checkpoint_file}")
        logger.info(f"📊 Statistics File: {STATS_FILE}")
        logger.info("=" * 70)
        
        # Print skip reasons
        if self.stats['skipped'] > 0:
            logger.info("\n📋 SKIPPED REPOSITORIES (Reason Breakdown):")
            logger.info("-" * 70)
            skip_reasons = {}
            for repo in self.stats['skipped_repos']:
                reason = repo.get('reason', 'unknown')
                if reason not in skip_reasons:
                    skip_reasons[reason] = []
                skip_reasons[reason].append({
                    'url': repo.get('url', 'N/A'),
                    'feature_count': repo.get('feature_count', 'N/A')
                })
            
            for reason, repos in skip_reasons.items():
                logger.info(f"\n  ⏭️  {reason} ({len(repos)} repo(s)):")
                for repo in repos[:5]:  # Show first 5 examples
                    logger.info(f"     • {repo['url']} (Features: {repo['feature_count']})")
                if len(repos) > 5:
                    logger.info(f"     ... and {len(repos) - 5} more")
        
        # Print error details if any
        if self.stats['errors'] > 0:
            logger.info("\n⚠️  FAILED REPOSITORIES (Error Breakdown):")
            logger.info("-" * 70)
            for repo in self.stats['failed_repos'][:5]:  # Show first 5
                logger.info(f"  • {repo.get('url', 'N/A')}: {repo.get('error', 'Unknown error')}")
            if len(self.stats['failed_repos']) > 5:
                logger.info(f"  ... and {len(self.stats['failed_repos']) - 5} more errors")
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ Execution completed successfully")
        logger.info("=" * 70)
    
    def save_statistics(self):
        """Save detailed statistics to file"""
        try:
            with open(STATS_FILE, 'w') as f:
                json.dump(self.stats, f, indent=2)
            logger.info(f"📊 Statistics saved: {STATS_FILE}")
        except Exception as e:
            logger.error(f"⚠️  Failed to save statistics: {e}")
    
    def generate_results_csv(self):
        """Generate separate CSV files for cloned, skipped, and error repos"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            stats_stem = Path(STATS_FILE).stem
            
            # ===== 1. CLONED REPOS CSV =====
            if self.stats['cloned_repos']:
                cloned_csv = f"{stats_stem}_CLONED_{timestamp}.csv"
                cloned_data = []
                
                for repo in self.stats['cloned_repos']:
                    cloned_data.append({
                        'sno': repo.get('sno', ''),
                        'github_url': repo.get('url', ''),
                        'repo_name': repo.get('repo_name', ''),
                        'feature_count': repo.get('feature_count', '0'),
                        'validation_info': repo.get('validation', ''),
                        'status': 'SUCCESS'
                    })
                
                keys_cloned = ['sno', 'github_url', 'repo_name', 'feature_count', 'validation_info', 'status']
                with open(cloned_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys_cloned, quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    writer.writerows(cloned_data)
                logger.info(f"✅ Cloned repos CSV: {cloned_csv}")
                logger.info(f"   Records: {len(cloned_data)}")
            
            # ===== 2. SKIPPED REPOS CSV =====
            if self.stats['skipped_repos']:
                skipped_csv = f"{stats_stem}_SKIPPED_{timestamp}.csv"
                skipped_data = []
                
                for repo in self.stats['skipped_repos']:
                    reason = repo.get('reason', 'unknown')
                    
                    # Parse reason for clarity
                    if 'invalid_gherkin_content' in reason:
                        skip_reason = 'INVALID_GHERKIN'
                        detail = reason.replace('invalid_gherkin_content: ', '')
                    elif 'feature_count < 10' in reason:
                        skip_reason = 'LOW_FEATURE_COUNT'
                        detail = f"Feature count {repo.get('feature_count', 0)} < {MIN_FEATURE_COUNT}"
                    elif 'no_github_url' in reason:
                        skip_reason = 'NO_URL'
                        detail = 'Missing or invalid GitHub URL'
                    else:
                        skip_reason = reason
                        detail = reason
                    
                    skipped_data.append({
                        'sno': repo.get('sno', ''),
                        'github_url': repo.get('url', ''),
                        'repo_name': repo.get('repo_name', ''),
                        'feature_count': repo.get('feature_count', '0'),
                        'skip_reason': skip_reason,
                        'skip_details': detail
                    })
                
                keys_skipped = ['sno', 'github_url', 'repo_name', 'feature_count', 'skip_reason', 'skip_details']
                with open(skipped_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys_skipped, quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    writer.writerows(skipped_data)
                logger.info(f"⏭️  Skipped repos CSV: {skipped_csv}")
                logger.info(f"   Records: {len(skipped_data)}")
            
            # ===== 3. FAILED REPOS CSV =====
            if self.stats['failed_repos']:
                errors_csv = f"{stats_stem}_ERRORS_{timestamp}.csv"
                error_data = []
                
                for repo in self.stats['failed_repos']:
                    error_data.append({
                        'sno': repo.get('sno', ''),
                        'github_url': repo.get('url', ''),
                        'feature_count': repo.get('feature_count', '0'),
                        'error_message': repo.get('error', 'Unknown error')
                    })
                
                keys_errors = ['sno', 'github_url', 'feature_count', 'error_message']
                with open(errors_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys_errors, quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    writer.writerows(error_data)
                logger.info(f"❌ Failed repos CSV: {errors_csv}")
                logger.info(f"   Records: {len(error_data)}")
            
            # ===== SUMMARY =====
            logger.info(f"")
            logger.info(f"📊 CSV Export Summary:")
            logger.info(f"   ✅ Cloned: {self.stats['cloned']} repos → _CLONED_*.csv")
            logger.info(f"   ⏭️  Skipped: {self.stats['skipped']} repos → _SKIPPED_*.csv")
            logger.info(f"   ❌ Errors: {self.stats['errors']} repos → _ERRORS_*.csv")
            
        except Exception as e:
            logger.error(f"❌ Failed to generate results CSV: {e}")


def main():
    """Entry point with user input for CSV file and folder name"""
    global CSV_FILE, CLONED_REPOS_DIR, CHECKPOINT_FILE, LOG_FILE, STATS_FILE
    
    try:
        # Print welcome banner
        print("=" * 70)
        print("🚀 BDD Repository Cloner - Initialization")
        print("=" * 70)
        print()
        
        # Ask for CSV file
        default_csv = "seart-search-repos-consolidated-removed-duplicates-sorted-output.csv"
        csv_input = input(f"Enter CSV file name [{default_csv}]: ").strip()
        CSV_FILE = csv_input if csv_input else default_csv
        
        # Verify CSV file exists
        if not Path(CSV_FILE).exists():
            print(f"❌ Error: CSV file not found: {CSV_FILE}")
            sys.exit(1)
        
        print(f"✅ CSV file: {CSV_FILE}")
        print()
        
        # Ask for folder name
        default_folder = "cloned_repos"
        user_input = input(f"Enter folder name for cloned repositories [{default_folder}]: ").strip()
        CLONED_REPOS_DIR = user_input if user_input else default_folder
        
        print(f"✅ Folder name set to: {CLONED_REPOS_DIR}")
        
        # Initialize dynamic configurations
        CHECKPOINT_FILE = f".{CLONED_REPOS_DIR}_checkpoint.json"
        LOG_FILE = f"{CLONED_REPOS_DIR}_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        STATS_FILE = f"{CLONED_REPOS_DIR}_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Reconfigure logging with the new log file
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler()
            ],
            force=True  # Force reconfiguration
        )
        
        print(f"✅ Checkpoint file: {CHECKPOINT_FILE}")
        print(f"✅ Log file: {LOG_FILE}")
        print()
        print("=" * 70)
        print()
        
        cloner = RepositoryCloner(CSV_FILE, CLONED_REPOS_DIR, CHECKPOINT_FILE)
        cloner.run()
        
    except KeyboardInterrupt:
        logger.warning("⚠️  Execution interrupted by user")
        logger.info(f"💾 Checkpoint saved - resume with: python3 clone_bdd_repos_seart_tool-1.py")
        print("\n✅ State saved - you can resume by running the script again")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
