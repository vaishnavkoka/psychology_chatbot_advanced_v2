#!/usr/bin/env python3
"""
PyDriller BDD Feature Mining - Simple CLI
Prompts for GitHub repository URL, mines BDD features, saves to CSV
"""

import sys
from pathlib import Path

# Add parent (Mining) directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydriller_feature_miner import PyDrillerFeatureMiner
from mining_integration import setup_mining_environment


def validate_github_url(url: str) -> bool:
    """Validate GitHub URL format"""
    return url.startswith("https://github.com/") or url.startswith("git@github.com:")


def extract_repo_name_from_url(url: str) -> str:
    """Extract repository name from GitHub URL"""
    # Handle https://github.com/owner/repo or https://github.com/owner/repo.git
    if url.endswith(".git"):
        url = url[:-4]
    return url.split("/")[-1]


def mine_single_repository(repo_url: str, repo_name: str = None, branch: str = "main"):
    """Mine a single repository and save results to CSV"""
    
    print("\n" + "="*80)
    print("🔍 PyDriller BDD Feature Mining")
    print("="*80 + "\n")
    
    # Extract repo name from URL if not provided
    if not repo_name:
        repo_name = extract_repo_name_from_url(repo_url)
    
    print(f"Repository: {repo_name}")
    print(f"URL: {repo_url}")
    print(f"Branch: {branch}\n")
    
    try:
        # Setup environment
        print("Setting up environment...")
        setup_mining_environment()
        
        # Create miner
        miner = PyDrillerFeatureMiner(output_prefix=repo_name)
        
        # Mine repository
        print(f"Mining repository...")
        repo_data = miner.mine_repository(
            repo_url=repo_url,
            repo_name=repo_name,
            branch=branch
        )
        
        # Export results
        print(f"Exporting results to CSV...")
        miner._export_results()
        
        print("\n" + "="*80)
        print("✅ Mining Complete!")
        print("="*80)
        print(f"\n📊 Results Summary:")
        if repo_data:
            print(f"   Feature files found: {len(repo_data.get('feature_files', []))}")
            print(f"   Total scenarios: {repo_data.get('total_scenarios', 0)}")
            print(f"   Commits analyzed: {repo_data.get('commits_analyzed', 0)}")
            print(f"   Commits with features: {repo_data.get('commits_with_features', 0)}")
        
        print(f"\n📁 Output Files:")
        import os
        output_dir = Path("../mining_outputs")
        if output_dir.exists():
            csv_files = list(output_dir.glob(f"{repo_name}*.csv"))
            for csv_file in csv_files:
                print(f"   ✓ {csv_file.name}")
        
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during mining: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point - prompt for URL and mine"""
    
    print("\n" + "="*80)
    print("🚀 PyDriller BDD Feature Mining Tool")
    print("="*80)
    print("\nThis tool mines BDD feature files (.feature) from GitHub repositories")
    print("and saves results to CSV files.\n")
    
    # Get repository URL
    while True:
        repo_url = input("📍 Enter GitHub repository URL: ").strip()
        
        if not repo_url:
            print("❌ URL cannot be empty. Try again.\n")
            continue
        
        if not validate_github_url(repo_url):
            print("❌ Invalid GitHub URL. Use format: https://github.com/owner/repo\n")
            continue
        
        break
    
    # Get optional repository name
    suggested_name = extract_repo_name_from_url(repo_url)
    repo_name_input = input(f"📝 Repository name [{suggested_name}]: ").strip()
    repo_name = repo_name_input if repo_name_input else suggested_name
    
    # Get optional branch
    branch = input("🌿 Branch name [main]: ").strip() or "main"
    
    # Mine the repository
    mine_single_repository(repo_url, repo_name, branch)
    
    # Ask if user wants to mine another
    while True:
        again = input("\n⚡ Mine another repository? (yes/no): ").strip().lower()
        if again in ["yes", "y"]:
            main()
            break
        elif again in ["no", "n"]:
            print("\n👋 Thank you for using PyDriller BDD Mining!\n")
            break
        else:
            print("❌ Please enter 'yes' or 'no'\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Mining cancelled by user.")
        sys.exit(0)
