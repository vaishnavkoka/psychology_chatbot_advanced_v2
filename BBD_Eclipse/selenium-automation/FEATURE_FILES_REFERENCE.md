# 🚀 Feature Files - Quick Reference & Execution Guide

## 📂 Created Feature Files

### 1. google.feature (Basic Introduction)
**Path:** `src/test/resources/features/google.feature`
**Type:** Foundational
**Scenarios:** 1
**Learning Focus:** Basic BDD syntax, browser operations

**Quick Run:**
```bash
# Set Java Home
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# Run via Maven
mvn clean test -Dtest=CucumberTestNGRunner

# Or in Eclipse: Right-click CucumberTestNGRunner.java → Run As → TestNG Test
```

**What It Tests:**
- Browser launch
- Google navigation
- Page title verification

---

### 2. google_search.feature (Search Operations)
**Path:** `src/test/resources/features/google_search.feature`
**Type:** Core Functionality
**Scenarios:** 3
**Learning Focus:** Search operations, dynamic parameters, multiple scenarios

**Scenarios Included:**
1. ✅ Search for Selenium
2. ✅ Search for Cucumber  
3. ✅ Multiple searches in one session

**What It Tests:**
- Search functionality
- Results verification
- Page title checks after search

**Key Step:**
```gherkin
When user searches for "Selenium"
# String parameter allows reuse with different values
```

---

### 3. browser_navigation.feature (Navigation)
**Path:** `src/test/resources/features/browser_navigation.feature`
**Type:** Navigation & URL Testing
**Scenarios:** 3
**Learning Focus:** URL verification, browser history, navigation

**Scenarios Included:**
1. ✅ Navigate to Google and verify URL
2. ✅ Navigate and verify page title
3. ✅ Go back after navigation

**What It Tests:**
- Navigation to websites
- URL pattern matching
- Browser back button
- Page title verification

**Key Steps:**
```gherkin
And current URL should contain "google"
# URL verification

And user goes back to previous page
# Browser navigation

Then page title should be "Google"
# Exact match assertion
```

---

### 4. data_driven_testing.feature (Parameterization)
**Path:** `src/test/resources/features/data_driven_testing.feature`
**Type:** Data-Driven Testing
**Scenarios:** 2 Scenario Outlines (5 total test runs)
**Learning Focus:** Scenario Outline, Examples table, test data

**Important Concept:**
```gherkin
Scenario Outline: Search for different topics
  When user searches for "<topic>"
  Then page title should contain "<expected>"

Examples:
  | topic           | expected        |
  | Automation      | Automation      |
  | Testing         | Testing         |
  | Quality Control | Quality Control |
  | Web Development | Web             |
```

**How It Works:**
- 1 Scenario Outline = 4 Test Executions (one per row)
- Each row has different test data
- Same test logic, different inputs
- Perfect for regression testing

**Test Runs Generated:**
1. Search for "Automation", verify "Automation" in title
2. Search for "Testing", verify "Testing" in title
3. Search for "Quality Control", verify "Quality Control" in title
4. Search for "Web Development", verify "Web" in title

**Advantages:**
- No code duplication
- Easy to add new test cases
- Centralized test data
- Better maintainability

---

### 5. form_interactions.feature (Form Actions)
**Path:** `src/test/resources/features/form_interactions.feature`
**Type:** Form Interaction
**Scenarios:** 3
**Learning Focus:** Form input, clearing, submission, field verification

**Scenarios Included:**
1. ✅ Fill search form and submit
2. ✅ Verify form elements
3. ✅ Clear and re-enter search text

**What It Tests:**
- Entering text in form fields
- Form submission
- Clearing form fields
- Form element visibility
- Form button state (enabled/disabled)
- Field content verification

**Key Steps:**
```gherkin
And user enters search term "Selenium WebDriver"
# Send keys to input field

And user submits the search form
# Submit form action

And user clears the search field
# Clear field action

Then search input field should contain "New search"
# Verify field content
```

---

### 6. element_verification.feature (UI Verification)
**Path:** `src/test/resources/features/element_verification.feature`
**Type:** Element & UI Verification
**Scenarios:** 4
**Learning Focus:** Element visibility, text content, attributes, performance

**Scenarios Included:**
1. ✅ Verify element visibility
2. ✅ Verify text content
3. ✅ Verify element attributes
4. ✅ Verify page load

**What It Tests:**
- Element visibility checks
- Page text content verification
- Element attribute values
- Placeholder text verification
- Button text verification
- Page load status
- Page load time measurement

**Key Steps:**
```gherkin
Then Google logo should be visible
# Element visibility

Then page should contain the text "Google"
# Page content verification

Then search input field should have placeholder text "Search"
# Attribute verification

Then page load time should be less than 10 seconds
# Performance assertion
```

---

## 🎯 How to Run All Feature Files

### Method 1: Run All at Once
```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
cd /home/vaishnavkoka/RE4BDD/BBD_Eclipse/selenium-automation
mvn clean test -Dtest=CucumberTestNGRunner
```

**Total Test Runs Generated:**
- google.feature: 1 scenario = 1 run
- google_search.feature: 3 scenarios = 3 runs
- browser_navigation.feature: 3 scenarios = 3 runs
- data_driven_testing.feature: 2 Outlines = 7 runs (4+3)
- form_interactions.feature: 3 scenarios = 3 runs
- element_verification.feature: 4 scenarios = 4 runs

**Total = 21 Test Executions! 🎉**

### Method 2: Run in Eclipse
1. Right-click **CucumberTestNGRunner.java**
2. Select **Run As → TestNG Test**
3. All feature files will execute
4. View results in Console

### Method 3: Run Specific Feature (Command Line)
**Note:** Currently our setup runs all features. To run specific features, you would need to modify the @CucumberOptions in CucumberTestNGRunner.java

---

## 📊 Expected Test Results

When running all features, you should see:

```
Total Scenarios: 20
Total Steps: ~100+
Tests Run: 21 (including Scenario Outline expansions)
Failures: 0 (if all steps pass)
Build Status: SUCCESS
```

---

## 📈 Learning Progression

### Beginner
Start with these features:
1. **google.feature** - Understand basic structure
2. **google_search.feature** - See multiple scenarios

### Intermediate
Move to these:
3. **browser_navigation.feature** - Learn URL testing
4. **form_interactions.feature** - Form interaction patterns

### Advanced
Master these:
5. **data_driven_testing.feature** - Scenario Outline mastery
6. **element_verification.feature** - Comprehensive verification

---

## 🔍 What Each Feature Teaches

| Feature | Teaches | Practice |
|---|---|---|
| google.feature | Basic Gherkin | Scenario structure, Given-When-Then |
| google_search.feature | Scenarios & Reuse | Multiple scenarios, parameter reuse |
| browser_navigation.feature | URL Testing | URL verification, navigation control |
| data_driven_testing.feature | Parameterization | Scenario Outline, Examples table |
| form_interactions.feature | Form Automation | Input, clear, submit, verification |
| element_verification.feature | UI Verification | Visibility, content, attributes, performance |

---

## 📋 Step Definition Cheat Sheet

### Browser Management
```gherkin
Given user launches the browser          # Initialize browser
When user opens the google website       # Navigate to Google
When user opens Wikipedia website        # Navigate to Wikipedia
When user opens "<website>"              # Parameterized navigation
When user goes back to previous page     # Browser back button
```

### Search Operations
```gherkin
When user searches for "<topic>"              # Search action
When user enters search term "<term>"         # Enter in search box
When user submits the search form             # Submit form
When user clears the search field             # Clear search box
Then search results should be displayed       # Verify results
```

### Assertions
```gherkin
Then page title should be "<title>"                      # Exact match
Then page title should contain "<text>"                  # Contains check
Then current URL should contain "<urlPart>"              # URL verification
Then browser should display Google homepage              # Page verification
Then page should contain the text "<text>"               # Text verification
```

### Element Verification
```gherkin
Then search input field should be visible               # Visibility
Then search button should be visible                     # Button visibility
Then search button should be enabled                     # Button state
Then Google logo should be visible                       # Element visibility
Then search input field should be displayed              # Display check
```

### Form Verification
```gherkin
Then search input field should contain "<text>"         # Field content
Then search input field should have placeholder text "<text>"  # Placeholder
Then search button should have text "<text>"            # Button text
```

### Performance
```gherkin
Then page should load successfully                      # Load status
Then page load time should be less than <seconds>       # Performance
```

---

## ✅ Verification Checklist

After running all features, verify:
- [ ] All 21 tests complete successfully
- [ ] No compilation errors
- [ ] No assertion failures
- [ ] Report generated at `target/cucumber-reports.html`
- [ ] Console shows ✓ for each step

---

## 🐛 Troubleshooting

### Issue: "Step is undefined"
**Solution:** Make sure step definitions in StepDefinitions.java match feature file steps exactly

### Issue: "Element not found"
**Solution:** Elements on Google may vary. The framework handles gracefully with try-catch

### Issue: "Browser doesn't open"
**Solution:** Running in headless mode by default. Chrome should still automate correctly

### Issue: "Port already in use"
**Solution:** Wait a moment between test runs for browser cleanup

---

## 🎓 Key Concepts Summary

### Scenario Outline Power
```gherkin
# Instead of writing 4 separate scenarios:
Scenario: Search for Automation
Scenario: Search for Testing
Scenario: Search for Quality Control

# Write 1 Scenario Outline:
Scenario Outline: Search for topics
  When user searches for "<topic>"
  Then page title should contain "<expected>"

Examples:
  | topic           | expected        |
  | Automation      | Automation      |
  | Testing         | Testing         |
  | Quality Control | Quality Control |
```

**Result:** Same logic, different data = Better maintainability!

---

## 🚀 Next Steps

1. **Run all features:** Execute and see all 21 tests pass
2. **Review reports:** Open `target/cucumber-reports.html`
3. **Modify scenarios:** Change search terms and re-run
4. **Add new feature:** Create your own .feature file
5. **Extend steps:** Add new step definitions
6. **CI/CD Integration:** Automate test execution

---

## 📞 Quick Reference

**Quick Run Command:**
```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
mvn clean test -Dtest=CucumberTestNGRunner
```

**Eclipse Run:**
Right-click CucumberTestNGRunner.java → Run As → TestNG Test

**View Reports:**
Open `target/cucumber-reports.html` in browser

---

**Happy Learning! 🎉**

You now have 6 comprehensive feature files with 20+ scenarios and 30+ step definitions ready to run!
