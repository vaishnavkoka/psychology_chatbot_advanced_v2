# Why You Cannot Run google.feature Directly

## The Problem

When you right-click on `google.feature` in Eclipse and try to run it, you get an error because:

1. **Feature files are NOT executable** - `.feature` files contain Gherkin (a human-readable syntax), not Java code
2. **They require a test runner** - You need a Java class (JUnit or TestNG runner) to interpret the feature and execute the steps
3. **Eclipse doesn't recognize .feature files as runnable** - Without the Cucumber IDE plugin, Eclipse treats them as plain text

## The Solution - Use the Runners We Created

Your feature file (`google.feature`) is now runnable through the test runners:

### ✅ Method 1: Run via CucumberTestNGRunner (Recommended)

**In Eclipse:**
1. Right-click on `com.selenium.CucumberTestNGRunner` class
2. Select **Run As → TestNG Test**
3. OR: Select **Run As → Java Application**

**Via Command Line:**
```bash
./mvnw clean test -Dtest=CucumberTestNGRunner
```

### ✅ Method 2: Run via RunCucumberTest (JUnit)

**In Eclipse:**
1. Right-click on `com.selenium.RunCucumberTest` class
2. Select **Run As → JUnit Test**

**Via Command Line:**
```bash
./mvnw clean test -Dtest=RunCucumberTest
```

### ✅ Method 3: Run All Tests

**In Eclipse:**
1. Right-click on project
2. Select **Run As → Maven test**

**Via Command Line:**
```bash
./mvnw test
```

## Understanding the Architecture

```
google.feature (Gherkin - NOT directly runnable)
        ↓ (defines steps)
        ↓
StepDefinitions.java (Java implementation of steps)
        ↓ (matched by runner)
        ↓
CucumberTestNGRunner.java (TestNG test class - RUNNABLE)
        ↓ (executed by)
        ↓
Maven/Surefire (test executor)
```

## Why You See Question Marks on Files

The question marks (?) in Eclipse appear because:

1. **Files created externally** - We created several new files via command line/IDE not through Eclipse GUI
2. **Maven needs to rebuild** - Eclipse hasn't indexed the new files yet
3. **Git tracking issues** - New files haven't been git-tracked

### Fix Question Marks:

**Solution 1: Refresh Eclipse Project**
1. Right-click on project → **Refresh** (or press F5)
2. Right-click on project → **Maven → Update Project** (Ctrl+Alt+U)
3. Wait for indexing to complete

**Solution 2: Clean and Rebuild**
1. Right-click on project → **Maven → Clean**
2. Right-click on project → **Maven → Update Project**
3. Project → **Clean** → **Rebuild All**

**Solution 3: Git Add New Files (if using Git)**
```bash
cd /home/vaishnavkoka/RE4BDD/BBD_Eclipse/selenium-automation
git add .
git commit -m "Add Cucumber setup and Maven Wrapper"
```

**Solution 4: Close and Reopen Eclipse Project**
1. Right-click project → **Close Project**
2. Right-click project → **Open Project**
3. If still not fixed, close Eclipse completely and reopen

## How Feature Files Work in BDD

**google.feature:**
```gherkin
Feature: Google Search
Scenario: Open Google and verify title
  Given user launches the browser
  When user opens the google website
  Then page title should be printed in console
```

**Execution Flow:**
1. Cucumber reads `.feature` file
2. Matches each Gherkin step to a method in `StepDefinitions.java`
3. Executes the corresponding Java code
4. Reports results

## Installing Cucumber IDE Plugin (Optional)

For better Eclipse support, you can install the Cucumber IDE plugin:

1. **Eclipse → Help → Eclipse Marketplace**
2. Search for "Cucumber"
3. Install "Cucumber Eclipse" or "Natural" plugin
4. After installation, you can run `.feature` files directly with better syntax highlighting

**Note:** This is optional - the runners we created will work regardless.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No runnable methods" on .feature | Right-click on `CucumberTestNGRunner.java` instead |
| "Cannot find main method" | Use `Run As → TestNG Test` not `Run As → Java Application` |
| "Step definitions not found" | Check glue path in `CucumberTestNGRunner.java` matches package |
| "Feature file not found" | Verify `src/test/resources/features/google.feature` exists |
| Question marks still showing | Wait 30 seconds for Eclipse indexing, then F5 refresh |

## Quick Reference

**To run your Cucumber tests, always use:**
- 🟢 Right-click `CucumberTestNGRunner.java` → Run As → TestNG Test
- 🟢 Command: `./mvnw clean test -Dtest=CucumberTestNGRunner`

**NOT:**
- ❌ Right-click `google.feature` and try to run
- ❌ Double-click `google.feature` (it's text, not executable)
