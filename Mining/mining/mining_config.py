# Mining Configuration for BDD OSS Projects
# This module contains configuration settings for the mining pipeline

MINING_CONFIG = {
    # GitHub API settings
    "github": {
        "base_api_url": "https://api.github.com",
        "search_language": "gherkin",
        "min_stars": 50,  # Minimum stars to filter quality projects
        "per_page": 100,
    },
    
    # BDD artifact criteria
    "bdd_criteria": {
        "min_feature_files": 4,  # Minimum number of feature files per project
        "feature_file_extension": ".feature",
        "step_definition_patterns": [
            r".*step.*\.py",      # Python: step_definitions.py, steps.py, etc.
            r".*step.*\.js",      # JavaScript: step_definitions.js, steps.js
            r".*step.*\.java",    # Java: StepDefinitions.java, Steps.java
            r".*glue.*\.java",    # Java: Glue files
            r".*spec.*\.rb",      # Ruby: spec files
        ],
    },
    
    # File patterns to look for
    "file_patterns": {
        "feature": "**/*.feature",
        "step_python": "**/*step*.py",
        "step_javascript": "**/*step*.js",
        "step_java": "**/*Step*.java",
        "step_ruby": "**/*spec*.rb",
        "requirements": ["**/*requirement*.txt", "**/*requirement*.md", "**/README.md"],
    },
    
    # Mining limits for pilot
    "pilot_limits": {
        "max_projects_to_scan": 50,  # For pilot, limit GitHub search
        "max_concurrent_clones": 5,
        "clone_timeout_seconds": 300,
        "max_feature_files_per_project": 20,  # Limit extraction
    },
    
    # Output settings
    "output": {
        "dataset_format": "csv",
        "output_dir": "./mining_outputs",
        "dataset_filename": "bdd_oss_mining_dataset.csv",
        "metadata_filename": "mining_metadata.json",
    },
}

# CSV column definitions
CSV_COLUMNS = [
    "project_id",
    "project_name",
    "project_url",
    "github_stars",
    "language",
    "feature_file_count",
    "feature_file_name",
    "requirement_id",
    "requirement_text",
    "step_definitions_found",
    "step_definitions_language",
    "feature_file_url",
    "step_definitions_url",
    "mining_timestamp",
]

# Search queries for GitHub
GITHUB_SEARCH_QUERIES = [
    'filename:*.feature stars:>50 language:gherkin',
    'path:features/*.feature stars:>50',
    'path:feature-files/*.feature stars:>50',
    'repo:cucumber/* .feature',
    'repo:behave/* .feature',
]
