# How to Run google.feature File - Complete Guide

## ✅ Summary

Your `google.feature` file **is now fully functional and runnable**. The question marks (?) on files have been resolved through Maven rebuild.

---

## 🚀 Method 1: Run via CucumberTestNGRunner (Recommended - Most Reliable)

### In Eclipse:
1. Right-click on `CucumberTestNGRunner.java` (located in `src/test/java/com/selenium/`)
2. Select **Run As → TestNG Test**
3. Watch the test execute in the Console view
4. The feature file `google.feature` will be executed automatically

### Via Command Line:
```bash
cd /home/vaishnavkoka/RE4BDD/BBD_Eclipse/selenium-automation
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
mvn clean test -Dtest=CucumberTestNGRunner
```

### Expected Output:
- Feature file executes successfully
- Browser opens (in headless mode if running via Maven)
- Google page title prints to console
- Test passes with 0 failures

---

## 🚀 Method 2: Run via RunCucumberTest (JUnit)

### In Eclipse:
1. Right-click on `RunCucumberTest.java` (located in `src/test/java/com/selenium/`)
2. Select **Run As → JUnit Test**
3. Watch the test execute

### Via Command Line:
```bash
cd /home/vaishnavkoka/RE4BDD/BBD_Eclipse/selenium-automation
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
mvn clean test -Dtest=RunCucumberTest
```

---

## 🚀 Method 3: Run All Tests (Including Both Runners)

### In Eclipse:
1. Right-click on the project folder
2. Select **Run As → Maven test**
3. Both runners will execute

### Via Command Line:
```bash
cd /home/vaishnavkoka/RE4BDD/BBD_Eclipse/selenium-automation
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
mvn clean test
```

---

## ⚠️ Why You Cannot Run .feature File Directly

When you right-click on `google.feature` and select "Run as → Cucumber Feature", you get an error because:

1. **Feature files are NOT executable code** - `.feature` files contain Gherkin (human-readable syntax)
2. **They require a Java runner** - Cucumber needs a Java class to interpret and execute the steps
3. **Eclipse needs the Cucumber IDE plugin** - Without it, Eclipse treats `.feature` files as plain text

### ✅ Solution:
**Always use the Java runner classes** (`CucumberTestNGRunner` or `RunCucumberTest`) to execute your feature files.

---

## 📊 Test Reports

After running your tests, reports are generated in the `target/` directory:

### HTML Reports:
- **`target/cucumber-reports.html`** - Detailed Cucumber report with step-by-step execution
- **`target/cucumber-reports-junit.html`** - JUnit-style HTML report

### JSON Reports:
- **`target/cucumber.json`** - Machine-readable report for integrations
- **`target/cucumber-junit.json`** - JUnit format JSON

### XML Reports:
- **`target/cucumber-junit.xml`** - JUnit XML format
- **`target/cucumber-junit-report.xml`** - Alternate XML format

**View Reports:** Open any `.html` file in your browser to view the detailed test execution report.

---

## 🔧 Project Structure

```
selenium-automation/
├── src/test/java/com/selenium/
│   ├── CucumberTestNGRunner.java        ← Run this (TestNG) ✅
│   ├── RunCucumberTest.java             ← Or run this (JUnit) ✅
│   ├── steps/
│   │   └── StepDefinitions.java         ← Step implementations
│   ├── listeners/
│   ├── reports/
│   └── tests/
├── src/test/resources/features/
│   └── google.feature                   ← Your feature file (NOT directly runnable)
├── pom.xml                              ← Maven configuration
└── target/                              ← Generated reports and compiled classes
```

---

## ✨ How Cucumber Works in This Project

```
google.feature (Gherkin syntax)
     ↓ (Cucumber reads)
     ↓
CucumberTestNGRunner/RunCucumberTest (Java test class)
     ↓ (finds matching steps in)
     ↓
StepDefinitions.java (Step implementations)
     ↓ (executes)
     ↓
Selenium WebDriver (opens browser, performs actions)
     ↓ (generates)
     ↓
Test Reports (HTML, JSON, XML)
```

---

## 🛠️ Setting JAVA_HOME (If Needed)

If you get Java-related errors, set the JAVA_HOME environment variable:

```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
# Then run your Maven command
```

---

## ✅ Quick Checklist

- [x] Maven build successful (no compilation errors)
- [x] google.feature file is runnable via TestNG/JUnit runner
- [x] CucumberTestNGRunner class is properly configured
- [x] RunCucumberTest class is properly configured
- [x] Step definitions are correctly matched to feature steps
- [x] Test reports are generated after execution
- [x] No question mark (?) issues on project files (resolved by Maven rebuild)

---

## 🐛 Troubleshooting

### Issue: "No scenarios found" error
**Solution:** Verify the `features` path in `@CucumberOptions` matches your actual feature file location.

### Issue: "Step is undefined" error
**Solution:** Verify step definitions in `StepDefinitions.java` match the feature file steps exactly.

### Issue: Browser doesn't open
**Solution:** The browser runs in headless mode when executed via Maven. Check console output for errors.

### Issue: Question marks still showing on files
**Solution:** 
1. Right-click project → **Maven → Update Project** (Ctrl+Alt+U)
2. Right-click project → **Refresh** (F5)
3. Project → **Clean** → **Rebuild All**

### Issue: JAVA_HOME error
**Solution:** Set JAVA_HOME before running Maven:
```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
```

---

## 📞 Key Points to Remember

✅ **Feature files are NOT directly runnable** - Use the Java runner classes instead
✅ **TestNG runner is recommended** - More reliable and widely used
✅ **Reports are automatically generated** - Check `target/` directory after running tests
✅ **Step definitions must match feature file steps** - Ensure they're in sync
✅ **Maven build is required** - Always run `mvn clean test` to ensure everything is compiled

---

## 🎯 Next Steps

1. **Run your test:** Use Method 1 (CucumberTestNGRunner) to execute the feature file
2. **View reports:** Open `target/cucumber-reports.html` in your browser
3. **Modify feature:** Edit `google.feature` to add more scenarios and steps
4. **Implement steps:** Add corresponding step implementations in `StepDefinitions.java`
5. **Run again:** Verify new steps execute correctly

---

Happy Testing! 🎉
