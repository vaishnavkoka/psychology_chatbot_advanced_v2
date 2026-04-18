"""
Dataset Analysis Tool
Analyzes the generated CSV dataset from the BDD mining pipeline
"""

import pandas as pd
from pathlib import Path
import json


def analyze_mining_dataset():
    """Load and analyze the generated dataset"""
    
    dataset_path = Path("mining_outputs/bdd_oss_mining_dataset.csv")
    metadata_path = Path("mining_outputs/mining_metadata.json")
    
    if not dataset_path.exists():
        print("❌ Dataset not found. Run the mining pipeline first.")
        return
    
    # Load data
    df = pd.read_csv(dataset_path)
    
    # Load metadata
    metadata = {}
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)
    
    # Print summary
    print("\n" + "="*70)
    print("BDD MINING DATASET ANALYSIS")
    print("="*70)
    
    print("\n### DATASET OVERVIEW ###")
    print(f"Total rows: {len(df)}")
    print(f"Total unique projects: {df['project_id'].nunique()}")
    print(f"Total feature files: {df['feature_file_name'].nunique()}")
    print(f"Timestamp: {df['mining_timestamp'].iloc[0] if len(df) > 0 else 'N/A'}")
    
    if metadata:
        print("\n### MINING METADATA ###")
        print(f"Projects scanned: {metadata.get('total_projects_scanned', 'N/A')}")
        print(f"Valid projects found: {metadata.get('valid_projects_found', 'N/A')}")
        print(f"Total features extracted: {metadata.get('total_features_extracted', 'N/A')}")
    
    print("\n### PROJECTS IN DATASET ###")
    projects = df.groupby('project_name').agg({
        'project_id': 'first',
        'project_url': 'first',
        'github_stars': 'first',
        'language': 'first',
        'feature_file_count': 'first',
        'feature_file_name': 'count',
    }).rename(columns={'feature_file_name': 'rows_in_dataset'})
    
    print(projects.to_string())
    
    print("\n### FEATURE FILES ###")
    print(f"Total unique feature files: {df['feature_file_name'].nunique()}")
    print(f"\nFeature files by project:")
    feature_counts = df.groupby('project_name')['feature_file_name'].nunique()
    for proj, count in feature_counts.items():
        print(f"  - {proj}: {count} files")
    
    print("\n### REQUIREMENTS ###")
    print(f"Total unique requirements: {df['requirement_id'].nunique()}")
    print(f"Projects with requirements: {df[df['requirement_id'] != 'N/A']['project_id'].nunique()}")
    
    req_coverage = df.groupby('project_name')['requirement_id'].nunique()
    print(f"\nRequirement coverage by project:")
    for proj, count in req_coverage.items():
        print(f"  - {proj}: {count} requirements")
    
    print("\n### STEP DEFINITIONS ###")
    with_steps = df[df['step_definitions_found'] == True]
    print(f"Feature files with step definitions: {len(with_steps)} / {len(df)}")
    
    step_languages = df['step_definitions_language'].value_counts()
    print(f"\nStep definition languages:")
    for lang, count in step_languages.items():
        print(f"  - {lang}: {count}")
    
    print("\n### LANGUAGE DISTRIBUTION ###")
    languages = df['language'].value_counts()
    print(languages.to_string())
    
    print("\n### QUALITY METRICS ###")
    print(f"Average GitHub stars: {df['github_stars'].mean():.0f}")
    print(f"Min stars: {df['github_stars'].min()}")
    print(f"Max stars: {df['github_stars'].max()}")
    print(f"Median stars: {df['github_stars'].median():.0f}")
    
    print("\n### DATA QUALITY ###")
    print(f"Rows with requirement text: {len(df[df['requirement_text'].notna() & (df['requirement_text'] != '')])} / {len(df)}")
    print(f"Rows with step definitions: {len(df[df['step_definitions_found'] == True])} / {len(df)}")
    print(f"Rows with complete feature URL: {df['feature_file_url'].str.startswith('http').sum()} / {len(df)}")
    
    print("\n### SAMPLE DATA ###")
    print("\nFirst 3 rows:")
    print(df.head(3)[['project_name', 'feature_file_name', 'requirement_text', 'step_definitions_found']].to_string())
    
    print("\n" + "="*70)
    print(f"✓ Full dataset saved to: {dataset_path}")
    print(f"✓ For Excel: Open {dataset_path} directly or use pandas")
    print("="*70 + "\n")


if __name__ == "__main__":
    analyze_mining_dataset()
