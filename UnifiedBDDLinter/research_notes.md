# Research: cuke_linter vs gherkin-lint

## cuke_linter (Ruby-based)
- Primary focus: Gherkin/Cucumber linting
- File name matching: CRITICAL RULE
- Rule ID: probably "FeatureFileSameNameAsFeature" or similar

## gherkin-lint (JavaScript-based)
- Primary focus: Gherkin syntax validation  
- File name matching: YES, enforced
- Focus areas: naming conventions, formatting

## Common Rule: Feature Name Must Match File Name
- Feature file: "login_flow.feature"
- Feature block: "Feature: Login Flow" or similar
- ERROR: If they don't match (either case-insensitive or exact)
