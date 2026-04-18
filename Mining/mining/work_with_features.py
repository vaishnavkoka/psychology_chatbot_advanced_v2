"""
Real Features Dataset Guide & Expansion Tool
Work with the extracted feature files and expand your dataset
"""

import pandas as pd
from pathlib import Path
import json
from Mining.mining.mining_config import MINING_CONFIG


def load_and_review_dataset():
    """Load and review the real features dataset"""
    
    output_dir = Path(MINING_CONFIG["output"]["output_dir"])
    csv_path = output_dir / "bdd_oss_with_real_features.csv"
    
    if not csv_path.exists():
        print("❌ Dataset not found. Run mine_real_features.py first")
        return None
    
    df = pd.read_csv(csv_path)
    
    print("\n" + "="*80)
    print("REAL FEATURE FILES DATASET")
    print("="*80)
    
    # Basic info
    print(f"\n📊 DATASET OVERVIEW:")
    print(f"   Total rows:         {len(df)}")
    print(f"   Total projects:     {df['project_name'].nunique()}")
    print(f"   Total feature files: {df['feature_file_name'].nunique()}")
    print(f"   Total scenarios:    {df['scenario_count'].sum()}")
    print(f"   Total LOC:          {df['lines_of_code'].sum()}")
    
    # Projects
    print(f"\n🏢 PROJECTS ({df['project_name'].nunique()}):")
    for proj in df['project_name'].unique():
        proj_data = df[df['project_name'] == proj].iloc[0]
        proj_count = len(df[df['project_name'] == proj])
        proj_scenarios = df[df['project_name'] == proj]['scenario_count'].sum()
        print(f"   • {proj}")
        print(f"     Language:   {proj_data['language']}")
        print(f"     Stars:      {proj_data['github_stars']}")
        print(f"     Features:   {proj_count}")
        print(f"     Scenarios:  {proj_scenarios}")
    
    # Languages
    print(f"\n💻 LANGUAGES:")
    for lang in df['language'].unique():
        count = len(df[df['language'] == lang])
        print(f"   • {lang}: {count} features")
    
    # Feature names
    print(f"\n📋 FEATURES BY PROJECT:")
    for proj in df['project_name'].unique():
        features = df[df['project_name'] == proj]['feature_file_name'].tolist()
        print(f"   {proj}:")
        for feat in features:
            print(f"      - {feat}")
    
    # Scenario details
    print(f"\n🎬 SCENARIOS BY FEATURE:")
    for idx, row in df.iterrows():
        if row['scenario_names']:
            print(f"   {row['feature_file_name']}:")
            scenarios = row['scenario_names'].split(' | ')
            for scenario in scenarios:
                print(f"      • {scenario}")
    
    print("\n" + "="*80)
    
    return df


def analyze_and_export():
    """Analyze and export feature data"""
    
    output_dir = Path(MINING_CONFIG["output"]["output_dir"])
    csv_path = output_dir / "bdd_oss_with_real_features.csv"
    
    df = pd.read_csv(csv_path)
    
    # Export by language
    for lang in df['language'].unique():
        lang_df = df[df['language'] == lang]
        export_path = output_dir / f"features_{lang.lower()}.csv"
        lang_df.to_csv(export_path, index=False)
        print(f"✓ Exported {lang} features: {export_path}")
    
    # Export by project
    for proj in df['project_name'].unique():
        proj_df = df[df['project_name'] == proj]
        export_path = output_dir / f"features_{proj}.csv"
        proj_df.to_csv(export_path, index=False)
        print(f"✓ Exported {proj} features: {export_path}")


def show_sample_feature():
    """Display a sample feature file"""
    
    output_dir = Path(MINING_CONFIG["output"]["output_dir"])
    feature_dir = output_dir / "feature_files"
    
    # Find first feature file
    feature_files = list(feature_dir.rglob("*.feature")) + list(feature_dir.rglob("*.story"))
    
    if not feature_files:
        print("❌ No feature files found")
        return
    
    sample = feature_files[0]
    
    print("\n" + "="*80)
    print("SAMPLE FEATURE FILE")
    print("="*80)
    print(f"\nPath: {sample}\n")
    
    with open(sample, 'r') as f:
        content = f.read()
    print(content)
    
    print("\n" + "="*80 + "\n")


def how_to_expand():
    """Show how to expand the dataset"""
    
    print("\n" + "="*80)
    print("HOW TO EXPAND YOUR DATASET")
    print("="*80)
    
    print("""
1️⃣  ADD MORE PROJECTS
    Edit mine_real_features.py, in create_sample_features():
    
    Add to features dictionary:
    "myproject": {
        "project": {
            "id": 4,
            "name": "my-project",
            "full_name": "user/my-project",
            "url": "https://github.com/user/my-project",
            "stars": XXXX,
            "language": "Python",  # or JavaScript, Java, Ruby
        },
        "files": [
            {
                "name": "test.feature",
                "path": "features/test.feature",
                "url": "https://github.com/.../test.feature",
                "content": '''Feature: Test
    Scenario: Do something
        Given condition
    '''
            }
        ]
    }

2️⃣  FETCH FROM REAL GITHUB
    Option A: Download from GitHub raw content URLs
    Option B: Use GitHub API (requires token)
    Option C: Clone repositories locally
    
    See extract_real_features.py for GitHub integration

3️⃣  RUN MINING
    python3 mine_real_features.py
    
    Output:
    • mining_outputs/bdd_oss_with_real_features.csv
    • mining_outputs/feature_files/
    • mining_outputs/real_features_summary.json

4️⃣  ANALYZE IN PYTHON
    import pandas as pd
    df = pd.read_csv('mining_outputs/bdd_oss_with_real_features.csv')
    
    # Filter by language
    js_features = df[df['language'] == 'JavaScript']
    
    # Get projects with most scenarios
    print(df.groupby('project_name')['scenario_count'].sum())
    
    # Export specific project
    cucumber = df[df['project_name'] == 'cucumber-js']
    cucumber.to_csv('cucumber_features.csv', index=False)

5️⃣  ANALYZE FEATURE CODE
    # Parse scenario names
    df['scenarios'] = df['scenario_names'].str.split(' | ')
    
    # Extract feature keywords
    df['has_outline'] = df['scenario_names'].str.contains('Outline')
    
    # Count steps
    df['step_count'] = df['lines_of_code'] / 3  # Rough estimate

════════════════════════════════════════════════════════════════════════════════
DATASET STRUCTURE
════════════════════════════════════════════════════════════════════════════════

mining_outputs/
├─ bdd_oss_with_real_features.csv    ← Your research dataset
│  Fields: project_id, project_name, feature_description, 
│          scenario_count, lines_of_code, local_path, ...
│
├─ feature_files/                    ← Actual .feature files
│  ├─ cucumber-js/features/
│  │  ├─ calculator.feature
│  │  ├─ cucumber.feature
│  │  ├─ support/support.feature
│  │  └─ hooks/hooks.feature
│  ├─ behave/features/
│  │  ├─ runner.feature
│  │  ├─ steps/steps.feature
│  │  ├─ tags/tags.feature
│  │  └─ scenarios.feature
│  └─ jbehave/src/test/resources/stories/
│     ├─ login.story
│     ├─ search.story
│     ├─ profiles.story
│     └─ notifications.story
│
├─ real_features_summary.json        ← Statistics
│
├─ features_javascript.csv           ← By language
├─ features_python.csv
├─ features_java.csv
│
└─ features_cucumber-js.csv          ← By project
   features_behave.csv
   features_jbehave.csv

════════════════════════════════════════════════════════════════════════════════
ANALYSIS EXAMPLES
════════════════════════════════════════════════════════════════════════════════

1. Count scenarios by project:
   df.groupby('project_name')['scenario_count'].agg(['sum', 'mean', 'count'])

2. Find longest feature:
   df.loc[df['lines_of_code'].idxmax()]

3. Compare languages:
   df.groupby('language').agg({
       'feature_file_name': 'count',
       'scenario_count': 'sum',
       'lines_of_code': 'mean'
   })

4. Export specific subset:
   python_features = df[df['language'] == 'Python']
   python_features.to_csv('python_bdd.csv')

════════════════════════════════════════════════════════════════════════════════
NEXT RESEARCH TOPICS
════════════════════════════════════════════════════════════════════════════════

📊 Metrics to Analyze:
   - Scenarios per feature (complexity)
   - Lines of code per scenario
   - Given/When/Then distribution
   - Use of Scenario Outline vs simple Scenario
   - Language-specific patterns
   - Project maturity (stars correlation)

📈 Research Questions:
   - How do BDD practices differ by language?
   - What's the average feature file size?
   - How many scenarios per project?
   - Are there naming conventions?
   - Do mature projects have more complex features?

🔍 Extract Next:
   - Given/When/Then steps per scenario
   - Data tables analysis
   - Tag usage patterns
   - Background clause usage
   - Example table complexity

✅ Validation:
   - All projects have ≥4 features: {df.groupby('project_name').size().min()} features minimum
   - All have scenarios: {df['scenario_count'].min()} scenarios minimum
   - All have content: {len(df[df['lines_of_code'] > 0])} with LOC > 0

════════════════════════════════════════════════════════════════════════════════
""")
    
    print("\n" + "="*80 + "\n")


def main():
    """Interactive menu"""
    
    print("\n" + "="*80)
    print("REAL FEATURES DATASET - TOOLS & GUIDE")
    print("="*80)
    print("""
What would you like to do?

1. Load and review the dataset
2. Analyze and export by language/project
3. Show a sample feature file
4. See how to expand the dataset
5. Exit
""")
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice == "1":
        load_and_review_dataset()
    elif choice == "2":
        analyze_and_export()
    elif choice == "3":
        show_sample_feature()
    elif choice == "4":
        how_to_expand()
    elif choice == "5":
        print("Goodbye!")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    # Auto-run analysis
    df = load_and_review_dataset()
    
    print("\nTo use additional tools, run this script and select from the menu.")
    print("Or use this in your Python code:")
    print("""
    from work_with_features import *
    df = load_and_review_dataset()
    """)
