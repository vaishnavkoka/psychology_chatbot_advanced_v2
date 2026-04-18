
# Complete Setup & Troubleshooting Guide

## ✅ Issues Fixed

### Issue 1: "Why can't I run google.feature directly?"

**Root Cause:**
- `.feature` files are NOT executable - they're plain text in Gherkin syntax
- They require a Java test runner (JUnit or TestNG) to execute
- Eclipse doesn't recognize `.feature` files as runnable without a special plugin

**Solution:**
Use the test runners we created instead. Feature files act as specifications that describe WHAT to test; runners/step definitions provide HOW to test.

### Issue 2: "Why are there question marks on files in Eclipse?"

**Root Cause:**
- New files created externally (command line) haven't been indexed by Eclipse yet
- Eclipse cache may be stale
- .settings folder contains metadata that Eclipse needs to refresh

**Solution:**
Performed automatic cleanup - see "Eclipse Cleanup Steps" below.

---

## 🚀 How to Run Cucumber Tests

### Method 1: Eclipse GUI (Recommended for Development)

**Option A: Run CucumberTestNGRunner Class**
```
1. In Project Explorer, navigate to: com.selenium → CucumberTestNGRunner
2. Right-click → Run As → TestNG Test
3. Watch the Console for test output
```

**Option B: Run from Toolbar**
```
1. Click on CucumberTestNGRunner class (in editor)
2. Click "Run" button in toolbar (or Ctrl+F11)
3. Select "TestNG Test" if prompted
```

**Option C: Run Test Suite via testng.xml**
```
1. Right-click on testng.xml
2. Run As → TestNG Suite
3. Executes all configured tests (Cucumber + FirstTest)
```

**Option D: Run via Maven (Eclipse)**
```
1. Right-click project → Maven → Run As → Maven build...
2. Goals: clean test -Dtest=CucumberTestNGRunner
3. Click Run
```

### Method 2: Command Line

```bash
# Navigate to project
cd /home/vaishnavkoka/RE4BDD/BBD_Eclipse/selenium-automation

# Run Cucumber tests only (TestNG runner)
./mvnw clean test -Dtest=CucumberTestNGRunner

# Run with Maven directly
mvn clean test -Dtest=CucumberTestNGRunner

# Run all tests (TestNG + Cucumber)
./mvnw test
```

### Method 3: Eclipse Launch Configuration

```
1. Click Run menu → Run Configurations
2. Find "Run Cucumber Tests"
3. Click Run button
```

---

## 📁 Project Files Explained

| File | Purpose |
|------|---------|
| `google.feature` | Gherkin BDD feature (what to test) |
| `CucumberTestNGRunner.java` | TestNG runner (primary) |
| `RunCucumberTest.java` | JUnit runner (alternative) |
| `StepDefinitions.java` | Step implementation (how to test) |
| `testng.xml` | TestNG suite configuration |
| `pom.xml` | Maven build configuration with Cucumber dependencies |
| `mvnw` / `mvnw.cmd` | Maven wrapper (no installation needed) |

---

## 🔧 Eclipse Cleanup Steps

**If you still see question marks or Eclipse shows errors:**

### Step 1: Refresh Project
```
1. Right-click project → Refresh (or press F5)
2. Wait 10-30 seconds for indexing
```

### Step 2: Update Maven
```
1. Right-click project → Maven → Update Project (Ctrl+Alt+U)
2. Check "Force Update of Snapshots/Releases"
3. Click OK
4. Wait for re-indexing
```

### Step 3: Clean and Rebuild
```
1. Project → Clean → Select "selenium-automation" → OK
2. Wait for rebuild
```

### Step 4: Full Eclipse Restart
```
1. File → Exit Eclipse
2. Delete: selenium-automation/.metadata (if exists)
3. Restart Eclipse
4. Open project again
```

---

## ✅ What's Working Now

- ✅ **Feature file is executable** through `CucumberTestNGRunner`
- ✅ **All question marks resolved** with updated Eclipse settings
- ✅ **Maven Wrapper working** - no Maven installation needed
- ✅ **TestNG integration** - compatible with existing TestNG setup
- ✅ **Git cleanup** - .gitignore prevents untracked files
- ✅ **Tests passing** - "Google" title printing confirmed

---

## 📊 Test Execution Flow

```
User Action (Eclipse GUI or Command Line)
        ↓
CucumberTestNGRunner / RunCucumberTest (Java Test Class)
        ↓
Maven Surefire / TestNG Provider
        ↓
Cucumber (reads .feature file)
        ↓
StepDefinitions.java (executes steps)
        ↓
Selenium WebDriver (launches browser, opens URL, captures output)
        ↓
Test Results (pass/fail + console output)
```

---

## 🎯 Common Tasks

### Run only Cucumber tests (not FirstTest.java)
```bash
./mvnw clean test -Dtest=CucumberTestNGRunner
```

### Run all tests
```bash
./mvnw test
```

### Run only FirstTest (TestNG test)
```bash
./mvnw clean test -Dtest=FirstTest
```

### Add a new feature
```
1. Create file: src/test/resources/features/new_feature.feature
2. Add Gherkin steps (Given/When/Then)
3. Add corresponding methods in StepDefinitions.java
4. Run: ./mvnw test -Dtest=CucumberTestNGRunner
```

### Run in debug mode
```bash
./mvnw -X clean test -Dtest=CucumberTestNGRunner
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No tests found" | Make sure you're running `CucumberTestNGRunner` class, not `.feature` file |
| "Step not implemented" | Add method to `StepDefinitions.java` with matching `@Given`/`@When`/`@Then` annotation |
| "Feature file not found" | Verify path: `src/test/resources/features/google.feature` |
| "Chrome not found" | Install Google Chrome or Chromium browser |
| "Permission denied" on mvnw | Run: `chmod +x mvnw` |
| Question marks still showing | Run: F5 refresh, then Maven → Update Project |
| "ClassNotFound" errors | Delete target/ folder: `rm -rf target/` then rebuild |

---

## 📖 Documentation Files

- **README.md** - General project setup and run instructions
- **SETUP_COMPLETE.md** - Detailed setup summary
- **WHY_FEATURE_NOT_RUNNABLE.md** - Explanation of feature file execution
- **This file** - Complete troubleshooting guide
- **testng.xml** - TestNG suite configuration
- **.eclipse/Run Cucumber Tests.launch** - Eclipse launch configuration

---

## ✨ Key Takeaways

1. **Feature files are NOT executable** - they're specifications (Gherkin syntax)
2. **Use test runners** - `CucumberTestNGRunner` (primary) or `RunCucumberTest` (alternative)
3. **Steps are defined in Java** - `StepDefinitions.java` provides implementation
4. **Run via Eclipse or Command Line** - multiple execution methods available
5. **Question marks = stale Eclipse cache** - F5 refresh + Maven update solves it
6. **Everything is working** - tests passing, output showing "Google"

---

## 🎉 You're All Set!

Your Cucumber BDD automation is fully configured and tested. Start by running:

```bash
./mvnw clean test -Dtest=CucumberTestNGRunner
```

Or in Eclipse:
```
Right-click CucumberTestNGRunner → Run As → TestNG Test
```

**Happy Testing!** 🚀
