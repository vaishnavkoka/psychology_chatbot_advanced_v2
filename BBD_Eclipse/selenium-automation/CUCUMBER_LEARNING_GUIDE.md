# 📚 Cucumber BDD Learning Guide

## Overview

This learning guide covers the feature files and step definitions created in the selenium-automation project. Each feature file teaches different Cucumber BDD concepts and Selenium automation patterns.

---

## 🎯 Feature Files Summary

| Feature File | Focus Area | Concepts Covered |
|---|---|---|
| `google.feature` | Basic Tests | Simple step definitions, basic assertions |
| `google_search.feature` | Search Functionality | Multiple scenarios, search operations |
| `browser_navigation.feature` | Navigation | URL verification, page title checks, browser history |
| `data_driven_testing.feature` | Parameterization | Scenario Outline, Examples, dynamic data |
| `form_interactions.feature` | Form Actions | Input, clear, submit, form element interaction |
| `element_verification.feature` | Element Verification | Visibility checks, text verification, attributes |

---

## 📖 Feature File Details

### 1. google.feature (Basic Introduction)
**File:** `src/test/resources/features/google.feature`

**Learning Concept:** Basic BDD with Cucumber
- Simple Given-When-Then syntax
- Browser launch and navigation
- Page title verification
- Basic cleanup

**Scenarios:**
- Open Google and verify title

**Key Learnings:**
```gherkin
Given user launches the browser    # Setup - @Given annotation
When user opens the google website # Action - @When annotation
Then page title should be printed  # Assertion - @Then annotation
```

---

### 2. google_search.feature (Search Operations)
**File:** `src/test/resources/features/google_search.feature`

**Learning Concept:** Multiple Scenarios & Search Actions
- Multiple scenarios in one feature file
- Search functionality testing
- Page title verification with search results

**Scenarios:**
1. Search for Selenium
2. Search for Cucumber
3. Multiple searches in one session

**Key Learnings:**
```gherkin
@When("user searches for {string}")
# Parameters (string) allow dynamic input
# Can be reused with different values

And user searches for "Selenium"
# Using "And" to continue the flow
```

**Step Definition Pattern:**
```java
@When("user searches for {string}")
public void user_searches_for(String searchTerm) {
    // Implementation uses parameter
}
```

---

### 3. browser_navigation.feature (Navigation & URLs)
**File:** `src/test/resources/features/browser_navigation.feature`

**Learning Concept:** Navigation and URL Verification
- Navigate to different websites
- Verify URL contains expected text
- Browser back button functionality
- URL assertion patterns

**Scenarios:**
1. Navigate to Google and verify URL
2. Navigate and verify page title
3. Go back after navigation

**Key Learnings:**
```gherkin
And current URL should contain "google"
# URL-based assertions

And user goes back to previous page
# Browser navigation history

Then page title should be "Google"
# Exact title match vs contains
```

**Advanced Concepts:**
```java
driver.navigate().back();              // Go back in browser history
driver.getCurrentUrl();                 // Get current URL
String title = driver.getTitle();       // Get page title
```

---

### 4. data_driven_testing.feature (Scenario Outline)
**File:** `src/test/resources/features/data_driven_testing.feature`

**Learning Concept:** Data-Driven Testing with Examples
- **Scenario Outline** for test parameterization
- **Examples** table for test data
- Reusable scenarios with different data
- Run multiple tests with minimal code

**Scenarios:**
1. Search for different topics (4 examples)
2. Verify URL patterns (3 examples)

**Key Learnings:**
```gherkin
Scenario Outline: Search for different topics
  When user searches for "<topic>"
  Then page title should contain "<expected>"

Examples:
  | topic           | expected        |
  | Automation      | Automation      |
  | Testing         | Testing         |
```

**How it Works:**
- Each row in Examples = 1 test execution
- First example → 1 test run
- Second example → 1 test run
- Third example → 1 test run
- Total = 3 test runs from 1 scenario outline!

**Advantages:**
- DRY (Don't Repeat Yourself) principle
- Easy to add new test data
- Centralized test data management
- Same scenario, different data

---

### 5. form_interactions.feature (Form Actions)
**File:** `src/test/resources/features/form_interactions.feature`

**Learning Concept:** Form Interactions & Element Manipulation
- Entering data in form fields
- Submitting forms
- Clearing form fields
- Re-entering new data

**Scenarios:**
1. Fill search form and submit
2. Verify form elements
3. Clear and re-enter search text

**Key Learnings:**
```gherkin
And user enters search term "Selenium WebDriver"
# Send text to input field

And user submits the search form
# Submit form

And user clears the search field
# Clear existing text

Then search input field should contain "New search"
# Verify field content
```

**Form Interaction Patterns:**
```java
WebElement searchBox = driver.findElement(By.name("q"));
searchBox.sendKeys("text");        // Enter text
searchBox.clear();                  // Clear field
searchBox.submit();                 // Submit form
String value = searchBox.getAttribute("value");  // Get field value
```

---

### 6. element_verification.feature (UI Verification)
**File:** `src/test/resources/features/element_verification.feature`

**Learning Concept:** Element Verification & UI Testing
- Verify element visibility
- Check text content
- Verify element attributes
- Page load verification
- Performance testing (load time)

**Scenarios:**
1. Verify element visibility
2. Verify text content
3. Verify element attributes
4. Verify page load

**Key Learnings:**
```gherkin
Then Google logo should be visible
# Element visibility check

Then page should contain the text "Google"
# Text content verification

Then search input field should have placeholder text "Search"
# Attribute verification

Then page load time should be less than 10 seconds
# Performance assertion
```

**Element Verification Patterns:**
```java
// Visibility check
assert searchBox.isDisplayed();

// Text verification
assert pageSource.contains("Google");

// Attribute verification
String placeholder = searchBox.getAttribute("placeholder");

// Page load check
String readyState = (String) executeScript("return document.readyState");

// Performance check
long loadTime = (endTime - startTime) / 1000;
```

---

## 🔍 Step Definition Categories

### Browser Management
```java
@Given("user launches the browser")
// Initializes ChromeDriver with options
// Enables headless mode for CI/CD
```

### Navigation Steps
```java
@When("user opens the google website")
@When("user opens Wikipedia website")
@When("user opens {string}")      // Parameterized
@When("user goes back to previous page")
```

### Search Operations
```java
@When("user searches for {string}")
@When("user enters search term {string}")
@When("user submits the search form")
@When("user clears the search field")
```

### Assertions & Verifications
```java
@Then("page title should be {string}")
@Then("page title should contain {string}")
@Then("search results should be displayed")
@Then("current URL should contain {string}")
```

### Element Verification
```java
@Then("search input field should be visible")
@Then("Google logo should be visible")
@Then("search button should be enabled")
@Then("page should contain the text {string}")
```

### Form Interactions
```java
@Then("search input field should contain {string}")
@Then("search button should have text {string}")
@Then("search input field should have placeholder text {string}")
```

### Performance Testing
```java
@Then("page should load successfully")
@Then("page load time should be less than {int} seconds")
```

---

## 🚀 How to Run Each Feature File

### Run Single Feature File
```bash
# Run only google_search.feature
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
mvn test -Dtest=CucumberTestNGRunner -Dcucumber.features="src/test/resources/features/google_search.feature"
```

### Run All Feature Files
```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
mvn clean test -Dtest=CucumberTestNGRunner
```

### Run in Eclipse
1. Right-click `CucumberTestNGRunner.java`
2. Select **Run As → TestNG Test**
3. All features will execute

---

## 📊 Understanding Test Reports

After running tests, check:
- **HTML Report:** `target/cucumber-reports.html`
- **JSON Report:** `target/cucumber.json`
- **XML Report:** `target/cucumber-junit.xml`

The HTML report shows:
- ✅ Passed scenarios (green)
- ❌ Failed scenarios (red)
- ⏭️ Skipped scenarios (blue)
- Step-by-step execution details
- Screenshots (if configured)

---

## 🎓 Key BDD Concepts Learned

### 1. Gherkin Syntax
```gherkin
Feature:     Business requirement description
Scenario:    Specific test case
Given:       Initial state / setup
When:        Action to perform
Then:        Expected result
And:         Additional steps in same level
```

### 2. Step Definitions
- Link between Gherkin and Java code
- Use annotations: `@Given`, `@When`, `@Then`, `@And`
- Support parameterization with `{string}`, `{int}`
- Reusable across multiple scenarios

### 3. Scenario Outline
- Template for data-driven testing
- Examples table provides test data
- One outline = multiple test runs
- Perfect for testing with different inputs

### 4. Parameterization Patterns
```gherkin
# String parameter
@When("user searches for {string}")
And user searches for "Selenium"

# Integer parameter
@Then("page load time should be less than {int} seconds")
Then page load time should be less than 5 seconds
```

### 5. Page Interaction Patterns
```java
// Find elements
WebElement element = driver.findElement(By.name("q"));

// Interact with elements
element.sendKeys("text");
element.click();
element.clear();
element.submit();

// Get element properties
element.isDisplayed();
element.isEnabled();
element.getAttribute("value");
```

---

## 💡 Best Practices

### 1. Feature File Organization
- One feature per functionality
- Clear, descriptive scenario names
- Use consistent terminology
- Keep scenarios independent

### 2. Step Definition Writing
- One responsibility per step
- Reusable across scenarios
- Clear parameter names
- Add logging/output for debugging

### 3. Test Data Management
- Use Scenario Outline for variations
- Keep test data centralized
- Avoid hardcoding URLs/credentials
- Use meaningful data values

### 4. Assertions
- Assert expected outcomes
- Use descriptive assertion messages
- Verify both positive and negative cases
- Check element properties before interaction

### 5. Error Handling
```java
try {
    // Action
} catch (Exception e) {
    System.out.println("✗ Action failed: " + e.getMessage());
}
```

---

## 🔧 Common Step Patterns

### URL Verification Pattern
```java
@Then("current URL should contain {string}")
public void verify_url(String urlPart) {
    String currentUrl = driver.getCurrentUrl();
    assert currentUrl.contains(urlPart);
}
```

### Element Visibility Pattern
```java
@Then("{string} should be visible")
public void verify_visibility(String elementName) {
    WebElement element = driver.findElement(locator);
    assert element.isDisplayed();
}
```

### Text Verification Pattern
```java
@Then("page should contain {string}")
public void verify_text(String text) {
    String pageSource = driver.getPageSource();
    assert pageSource.contains(text);
}
```

### Form Input Pattern
```java
@When("user enters {string}")
public void enter_text(String text) {
    WebElement field = driver.findElement(By.name("q"));
    field.clear();
    field.sendKeys(text);
}
```

---

## 📈 Learning Path

1. **Start:** `google.feature` - Understand basic structure
2. **Expand:** `google_search.feature` - Multiple scenarios
3. **Navigate:** `browser_navigation.feature` - URL testing
4. **Parameterize:** `data_driven_testing.feature` - Scenario Outline
5. **Interact:** `form_interactions.feature` - Form actions
6. **Verify:** `element_verification.feature` - UI verification

---

## 🎯 Next Steps

1. Run all feature files: See them execute successfully
2. Modify scenarios: Add your own test cases
3. Add new steps: Extend StepDefinitions.java
4. Create new features: Apply learned concepts
5. Integrate with CI/CD: Automate test execution

---

## 📚 Additional Resources

### Cucumber Documentation
- [Cucumber.io](https://cucumber.io/)
- [Gherkin Syntax](https://cucumber.io/docs/gherkin/reference/)

### Selenium Documentation
- [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
- [Locators Strategy](https://www.selenium.dev/documentation/webdriver/elements/locators/)

### BDD Concepts
- [Behavior-Driven Development](https://cucumber.io/docs/bdd/)
- [Given-When-Then Format](https://cucumber.io/docs/gherkin/reference/#steps)

---

## ✅ Checklist - Learning Progress

- [ ] Read and understand each feature file
- [ ] Run each feature file individually
- [ ] Review the test reports
- [ ] Understand Scenario Outline concept
- [ ] Modify a scenario and run it
- [ ] Add a new step definition
- [ ] Create your own feature file
- [ ] Run all tests together
- [ ] Generate and review reports

---

## 🎉 Congratulations!

You now have a comprehensive BDD automation framework with:
- ✅ 6 feature files covering different concepts
- ✅ 30+ step definitions
- ✅ Data-driven testing support
- ✅ Comprehensive element verification
- ✅ Form interaction patterns
- ✅ Performance testing capabilities
- ✅ Automatic test reporting

**Happy Testing! 🚀**
