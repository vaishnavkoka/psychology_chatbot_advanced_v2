"""
Pilot Mining Task - Proof of Concept
Demonstrates the mining pipeline with mock data and sample analysis
"""

import sys
from pathlib import Path
from Mining.mining.oss_bdd_mining import BDDMiningPipeline
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_sample_mining_data():
    """
    Generate sample mining data for demonstration
    This shows what the full pipeline would produce
    """
    print("\n" + "="*70)
    print("SAMPLE MINING DATA - What the full pipeline will extract")
    print("="*70)
    
    sample_data = {
        "project_1": {
            "name": "cucumber-js",
            "features": ["login.feature", "checkout.feature", "search.feature", "profile.feature"],
            "requirements": [
                "Users must authenticate before accessing the system",
                "Search functionality must return results in < 2 seconds",
                "Payment processing must be PCI compliant",
                "User profile must be updateable"
            ],
            "step_definitions": {
                "javascript": ["features/step_definitions/auth.steps.js", "features/step_definitions/checkout.steps.js"],
            }
        },
        "project_2": {
            "name": "behave",
            "features": ["api.feature", "validation.feature", "database.feature", "error_handling.feature"],
            "requirements": [
                "API endpoints must follow REST conventions",
                "Input validation must catch SQL injection attempts",
                "Database transactions must be ACID compliant",
                "Error responses must include helpful error messages"
            ],
            "step_definitions": {
                "python": ["features/steps/api_steps.py", "features/steps/db_steps.py"],
            }
        }
    }
    
    for proj_id, proj_data in sample_data.items():
        print(f"\n{proj_id.upper()}: {proj_data['name']}")
        print("-" * 70)
        print(f"  Features ({len(proj_data['features'])}): {', '.join(proj_data['features'])}")
        print(f"  Requirements ({len(proj_data['requirements'])}):")
        for i, req in enumerate(proj_data['requirements'], 1):
            print(f"    {i}. {req}")
        print(f"  Step Definitions: {proj_data['step_definitions']}")
    
    print("\n" + "="*70)
    print("CSV OUTPUT FORMAT")
    print("="*70)
    print("""
    Columns in generated CSV:
    - project_id: Unique project identifier
    - project_name: GitHub project name
    - project_url: GitHub repository URL
    - github_stars: Repository star count (quality indicator)
    - language: Primary language
    - feature_file_count: Total feature files in project
    - feature_file_name: Individual feature file name
    - requirement_id: Source requirement file
    - requirement_text: Extracted requirement text
    - step_definitions_found: Whether step implementations exist
    - step_definitions_language: Language of step definitions
    - feature_file_url: Direct link to feature file
    - step_definitions_url: Link to step definitions
    - mining_timestamp: When the data was extracted
    """)


def run_pilot_mining():
    """Run the pilot mining task with mock data"""
    print("\n" + "="*70)
    print("PILOT MINING TASK - Proof of Concept")
    print("="*70)
    print("\nThis pilot demonstrates:")
    print("  1. GitHub project discovery")
    print("  2. BDD artifact extraction (feature files)")
    print("  3. Requirements mapping")
    print("  4. Step definition identification")
    print("  5. CSV dataset generation")
    
    # Create and run pipeline with mock data
    pipeline = BDDMiningPipeline(use_mock_data=True)
    
    # Add sample data to simulate mining results
    pipeline.mining_results = [
        {
            "project": {
                "id": 1,
                "name": "cucumber-js",
                "full_name": "cucumber/cucumber-js",
                "url": "https://github.com/cucumber/cucumber-js",
                "clone_url": "https://github.com/cucumber/cucumber-js.git",
                "stars": 2500,
                "language": "JavaScript",
                "description": "Cucumber for JavaScript - BDD testing framework",
            },
            "feature_count": 4,
            "feature_files": [
                Path("features/authentication.feature"),
                Path("features/checkout.feature"),
                Path("features/search.feature"),
                Path("features/user_profile.feature"),
            ],
            "step_definitions": {
                "javascript": [
                    "features/step_definitions/authentication.steps.js",
                    "features/step_definitions/checkout.steps.js",
                ],
                "python": [],
                "java": [],
                "ruby": [],
            },
            "requirements": [
                {
                    "file": "REQUIREMENTS.md",
                    "content_preview": "User authentication must support OAuth2 and JWT tokens",
                },
                {
                    "file": "README.md",
                    "content_preview": "Checkout process must complete in under 30 seconds",
                },
            ]
        },
        {
            "project": {
                "id": 2,
                "name": "behave",
                "full_name": "behave/behave",
                "url": "https://github.com/behave/behave",
                "clone_url": "https://github.com/behave/behave.git",
                "stars": 2300,
                "language": "Python",
                "description": "Behavior-driven development for Python",
            },
            "feature_count": 4,
            "feature_files": [
                Path("features/api_endpoints.feature"),
                Path("features/data_validation.feature"),
                Path("features/database_operations.feature"),
                Path("features/error_handling.feature"),
            ],
            "step_definitions": {
                "python": [
                    "features/steps/api_steps.py",
                    "features/steps/db_steps.py",
                ],
                "javascript": [],
                "java": [],
                "ruby": [],
            },
            "requirements": [
                {
                    "file": "REQUIREMENTS.md",
                    "content_preview": "API must support REST operations: GET, POST, PUT, DELETE",
                },
                {
                    "file": "README.md",
                    "content_preview": "Database operations must maintain ACID compliance",
                },
            ]
        }
    ]
    
    # Generate dataset
    print("\n[Generating CSV Dataset]")
    pipeline.generate_csv_dataset()
    pipeline.save_metadata()
    
    # Show sample data info
    generate_sample_mining_data()
    
    # Print next steps
    print("\n" + "="*70)
    print("NEXT STEPS FOR FULL MINING")
    print("="*70)
    print("""
    1. SETUP:
       - Install dependencies: pip install -r mining_requirements.txt
       - Set GitHub token: export GITHUB_TOKEN=your_token (optional, for higher API limits)
    
    2. RUN FULL MINING (with real GitHub data):
       - Edit run_mining.py and set use_mock_data=False
       - Run: python run_mining.py
       - Monitor logs for progress
    
    3. ANALYZE RESULTS:
       - Open generated CSV in pandas or Excel
       - Script will extract feature files, map to requirements
       - Step definitions will be categorized by language
    
    4. VALIDATION:
       - Verify minimum 4 feature files per project
       - Check requirement mapping accuracy
       - Review step definition completeness
    
    5. EXPANSION:
       - Increase max_projects_to_scan in mining_config.py
       - Add more search queries for different frameworks
       - Enhance requirement extraction logic
    """)
    print("="*70 + "\n")


if __name__ == "__main__":
    run_pilot_mining()
