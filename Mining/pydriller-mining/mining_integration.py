"""
PyDriller + GitHub API Mining Integration
Combines PyDriller Git history mining with GitHub API feature file discovery
Creates unified dataset with feature evolution analysis
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from Mining.mining.mining_config import MINING_CONFIG
from pydriller_feature_miner import PyDrillerFeatureMiner


class BDDMiningIntegration:
    """Integrate PyDriller and GitHub API mining"""
    
    def __init__(self):
        self.output_dir = Path(MINING_CONFIG["output"]["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().isoformat()
    
    def run_integrated_mining(self, repositories: list) -> Dict:
        """
        Run integrated mining pipeline: GitHub API + PyDriller
        
        Args:
            repositories: List of repo configs with 'url', 'name', 'branch'
        """
        print(f"\n{'='*80}")
        print(f"🚀 INTEGRATED BDD MINING PIPELINE")
        print(f"{'='*80}\n")
        
        results = {
            "pydriller_mining": None,
            "integrated_dataset": None,
            "summary": {}
        }
        
        # Step 1: Run PyDriller mining
        print("📍 STEP 1: Running PyDriller Git history mining...\n")
        miner = PyDrillerFeatureMiner(output_prefix="integrated_bdd")
        miner.mine_multiple_repositories(repositories)
        results["pydriller_mining"] = miner
        
        # Step 2: Load PyDriller results
        print("\n📍 STEP 2: Loading PyDriller results...\n")
        pydriller_csv = self.output_dir / "integrated_bdd_features.csv"
        if pydriller_csv.exists():
            pydriller_df = pd.read_csv(pydriller_csv)
            print(f"✓ Loaded {len(pydriller_df)} feature files from PyDriller")
        else:
            print("⚠️  No PyDriller CSV found")
            pydriller_df = None
        
        # Step 3: Create integrated dataset
        print("\n📍 STEP 3: Creating integrated dataset...\n")
        
        if pydriller_df is not None:
            # Enhance with additional metrics
            integrated_df = self._enhance_dataset(pydriller_df, miner)
            
            # Export integrated dataset
            integrated_csv = self.output_dir / "integrated_bdd_mining_dataset.csv"
            integrated_df.to_csv(integrated_csv, index=False)
            print(f"✓ Created integrated dataset: {integrated_csv}")
            print(f"  Total rows: {len(integrated_df)}")
            print(f"  Columns: {', '.join(integrated_df.columns)}")
            
            results["integrated_dataset"] = integrated_df
            
            # Generate summary statistics
            self._generate_summary(integrated_df, miner, results["summary"])
        
        # Step 4: Export comprehensive report
        print("\n📍 STEP 4: Generating comprehensive report...\n")
        self._generate_report(results)
        
        return results
    
    def _enhance_dataset(self, df: pd.DataFrame, miner: PyDrillerFeatureMiner) -> pd.DataFrame:
        """Enhance PyDriller dataset with additional metrics"""
        
        enhanced_df = df.copy()
        
        # Add metadata columns if not present
        if 'extracted_at' not in enhanced_df.columns:
            enhanced_df['extracted_at'] = self.timestamp
        
        if 'mining_method' not in enhanced_df.columns:
            enhanced_df['mining_method'] = 'PyDriller'
        
        # Calculate feature stability (based on commit frequency)
        def calculate_stability(commits):
            if pd.isna(commits):
                return 'unknown'
            commits = int(commits)
            if commits < 2:
                return 'new'
            elif commits < 5:
                return 'emerging'
            elif commits < 15:
                return 'stable'
            else:
                return 'mature'
        
        enhanced_df['feature_stability'] = enhanced_df['commits'].apply(calculate_stability)
        
        # Add complexity score based on scenario count
        enhanced_df['complexity_score'] = enhanced_df['scenario_count'].apply(
            lambda x: 'low' if x < 3 else 'medium' if x < 10 else 'high'
        )
        
        return enhanced_df
    
    def _generate_summary(self, df: pd.DataFrame, miner: PyDrillerFeatureMiner, summary: dict) -> None:
        """Generate summary statistics"""
        
        summary['total_repositories'] = len(df['repo_name'].unique())
        summary['total_feature_files'] = len(df)
        summary['total_scenarios'] = df['scenario_count'].sum()
        summary['avg_scenarios_per_file'] = df['scenario_count'].mean()
        summary['commits_per_file_avg'] = df['commits'].mean()
        summary['stability_distribution'] = df['feature_stability'].value_counts().to_dict()
        summary['complexity_distribution'] = df['complexity_score'].value_counts().to_dict()
        summary['pydriller_stats'] = miner.stats
    
    def _generate_report(self, results: Dict) -> None:
        """Generate comprehensive mining report"""
        
        report_path = self.output_dir / "integrated_mining_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("INTEGRATED BDD MINING REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated: {self.timestamp}\n\n")
            
            # PyDriller Statistics
            if results['pydriller_mining']:
                miner = results['pydriller_mining']
                f.write("PYDRILLER MINING STATISTICS\n")
                f.write("-"*80 + "\n")
                for key, value in miner.stats.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
            
            # Summary Statistics
            if results['summary']:
                summary = results['summary']
                f.write("INTEGRATED DATASET SUMMARY\n")
                f.write("-"*80 + "\n")
                f.write(f"  Total repositories: {summary.get('total_repositories', 'N/A')}\n")
                f.write(f"  Total feature files: {summary.get('total_feature_files', 'N/A')}\n")
                f.write(f"  Total scenarios: {summary.get('total_scenarios', 'N/A')}\n")
                f.write(f"  Avg scenarios per file: {summary.get('avg_scenarios_per_file', 'N/A'):.2f}\n")
                f.write(f"  Avg commits per file: {summary.get('commits_per_file_avg', 'N/A'):.2f}\n")
                
                if 'stability_distribution' in summary:
                    f.write(f"\n  Feature Stability Distribution:\n")
                    for stability, count in summary['stability_distribution'].items():
                        f.write(f"    {stability}: {count}\n")
                
                if 'complexity_distribution' in summary:
                    f.write(f"\n  Complexity Score Distribution:\n")
                    for complexity, count in summary['complexity_distribution'].items():
                        f.write(f"    {complexity}: {count}\n")
                
                f.write("\n")
            
            # Dataset Overview
            if results['integrated_dataset'] is not None:
                df = results['integrated_dataset']
                f.write("DATASET COLUMNS\n")
                f.write("-"*80 + "\n")
                for col in df.columns:
                    f.write(f"  - {col}\n")
                
                f.write("\nTOP REPOSITORIES\n")
                f.write("-"*80 + "\n")
                top_repos = df['repo_name'].value_counts().head(10)
                for repo, count in top_repos.items():
                    f.write(f"  {repo}: {count} feature files\n")
                
                f.write("\nFEATURE FILES BY STABILITY\n")
                f.write("-"*80 + "\n")
                stability_groups = df.groupby('feature_stability').agg({
                    'scenario_count': 'sum',
                    'feature_file': 'count'
                }).rename(columns={'feature_file': 'count'})
                for stability, row in stability_groups.iterrows():
                    f.write(f"  {stability}: {int(row['count'])} files, {int(row['scenario_count'])} scenarios\n")
        
        print(f"✓ Generated report: {report_path}")


# Quick Start Functions

def setup_mining_environment():
    """Check and install PyDriller if needed"""
    print("🔍 Checking PyDriller installation...")
    try:
        import pydriller
        print("✓ PyDriller is installed")
        return True
    except ImportError:
        print("⚠️  PyDriller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pydriller"])
        print("✓ PyDriller installed successfully")
        return True


def run_quick_mining():
    """Quick start mining with popular BDD repositories"""
    
    repositories = [
        {
            "url": "https://github.com/cucumber/cucumber-js",
            "name": "cucumber-js",
            "branch": "main"
        },
        {
            "url": "https://github.com/behave/behave",
            "name": "behave",
            "branch": "master"
        },
        {
            "url": "https://github.com/apiaryio/dredd",
            "name": "dredd",
            "branch": "master"
        },
    ]
    
    integration = BDDMiningIntegration()
    results = integration.run_integrated_mining(repositories)
    
    return results


if __name__ == "__main__":
    # Check environment
    setup_mining_environment()
    
    # Run quick mining
    print("\n🚀 Starting BDD feature mining integration...\n")
    results = run_quick_mining()
    
    print("\n✅ Mining pipeline completed successfully!")
    print(f"📁 Results saved to: {MINING_CONFIG['output']['output_dir']}")
