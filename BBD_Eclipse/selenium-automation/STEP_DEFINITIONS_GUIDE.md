# 💻 Step Definition Examples & Best Practices

## Understanding Step Definitions

Step definitions are the Java code that connects your Gherkin scenarios to actual test actions.

### Basic Structure
```java
@Given("step description")
public void step_method_name() {
    // Implementation code
}
```

---

## 📝 Common Patterns & Examples

### 1. Browser Management Pattern

**Feature File:**
```gherkin
Given user launches the browser
```

**Step Definition:**
```java
@Given("user launches the browser")
public void user_launches_the_browser() {
    WebDriverManager.chromedriver().setup();
    ChromeOptions options = new ChromeOptions();
    
    // Enable headless for CI/CD
    String display = System.getenv("DISPLAY");
    String ci = System.getenv("CI");
    if (ci != null || display == null || display.isEmpty()) {
        options.addArguments("--headless=new");
        options.addArguments("--no-sandbox");
    }
    
    driver = new ChromeDriver(options);
    driver.manage().window().maximize();
    System.out.println("✓ Browser launched");
}
```

**Key Points:**
- Use WebDriverManager for automatic driver management
- Handle headless mode for CI/CD
- Maximize window for consistent testing
- Add logging for debugging

---

### 2. Navigation Pattern

**Feature File:**
```gherkin
When user opens the google website
When user opens "<website>"
When user goes back to previous page
```

**Step Definition:**
```java
@When("user opens the google website")
public void user_opens_the_google_website() {
    driver.get("https://www.google.com");
    System.out.println("✓ Navigated to Google");
}

@When("user opens {string}")
public void user_opens_website(String website) {
    driver.get("https://www." + website);
    System.out.println("✓ Navigated to " + website);
}

@When("user goes back to previous page")
public void user_goes_back_to_previous_page() {
    driver.navigate().back();
    System.out.println("✓ Navigated back");
}
```

**Key Points:**
- Use driver.get() for direct navigation
- Parameterize for flexibility
- Use driver.navigate().back() for history
- Log all actions

---

### 3. Form Interaction Pattern

**Feature File:**
```gherkin
And user enters search term "Selenium"
And user submits the search form
And user clears the search field
```

**Step Definition:**
```java
@When("user enters search term {string}")
public void user_enters_search_term(String searchTerm) {
    try {
        WebElement searchBox = driver.findElement(By.name("q"));
        searchBox.clear();
        searchBox.sendKeys(searchTerm);
        System.out.println("✓ Entered: " + searchTerm);
    } catch (Exception e) {
        System.out.println("✗ Error entering search: " + e.getMessage());
    }
}

@When("user submits the search form")
public void user_submits_the_search_form() {
    try {
        WebElement searchBox = driver.findElement(By.name("q"));
        searchBox.submit();
        System.out.println("✓ Form submitted");
        Thread.sleep(2000);  // Wait for page load
    } catch (Exception e) {
        System.out.println("✗ Error submitting form: " + e.getMessage());
    }
}

@When("user clears the search field")
public void user_clears_the_search_field() {
    try {
        WebElement searchBox = driver.findElement(By.name("q"));
        searchBox.clear();
        System.out.println("✓ Search field cleared");
    } catch (Exception e) {
        System.out.println("✗ Error clearing field: " + e.getMessage());
    }
}
```

**Key Points:**
- Always use try-catch for error handling
- Clear field before entering text
- Use submit() method instead of click() for forms
- Add wait time after form submission
- Log success and error messages

---

### 4. Assertion Pattern - Title Verification

**Feature File:**
```gherkin
Then page title should be "Google"
Then page title should contain "Google"
```

**Step Definition:**
```java
@Then("page title should be {string}")
public void page_title_should_be(String expectedTitle) {
    String actualTitle = driver.getTitle();
    assert actualTitle.equals(expectedTitle) 
        : "Title mismatch. Expected: " + expectedTitle + ", Got: " + actualTitle;
    System.out.println("✓ Title verified: " + actualTitle);
}

@Then("page title should contain {string}")
public void page_title_should_contain(String text) {
    String title = driver.getTitle();
    assert title.contains(text) 
        : "Title does not contain: " + text;
    System.out.println("✓ Title contains: " + text);
}
```

**Key Points:**
- Use .equals() for exact match
- Use .contains() for partial match
- Always include descriptive assertion messages
- Log the actual value for debugging

---

### 5. URL Verification Pattern

**Feature File:**
```gherkin
Then current URL should contain "google"
```

**Step Definition:**
```java
@Then("current URL should contain {string}")
public void current_url_should_contain(String urlPart) {
    String currentUrl = driver.getCurrentUrl();
    assert currentUrl.contains(urlPart) 
        : "URL does not contain: " + urlPart + ". Current URL: " + currentUrl;
    System.out.println("✓ URL contains: " + urlPart);
}
```

**Key Points:**
- Get current URL with driver.getCurrentUrl()
- Use .contains() for partial matching
- Include actual URL in assertion message

---

### 6. Element Visibility Pattern

**Feature File:**
```gherkin
Then search input field should be visible
Then Google logo should be visible
```

**Step Definition:**
```java
@Then("search input field should be visible")
public void search_input_field_should_be_visible() {
    try {
        WebElement searchBox = driver.findElement(By.name("q"));
        assert searchBox.isDisplayed() 
            : "Search input is not visible";
        System.out.println("✓ Search input is visible");
    } catch (NoSuchElementException e) {
        System.out.println("✗ Search input not found: " + e.getMessage());
    }
}

@Then("Google logo should be visible")
public void google_logo_should_be_visible() {
    try {
        WebElement logo = driver.findElement(By.id("hplogo"));
        assert logo.isDisplayed() 
            : "Google logo is not visible";
        System.out.println("✓ Google logo is visible");
    } catch (NoSuchElementException e) {
        System.out.println("✗ Google logo not found: " + e.getMessage());
    }
}
```

**Key Points:**
- Use isDisplayed() for visibility check
- Handle NoSuchElementException gracefully
- Include try-catch for robustness

---

### 7. Element State Verification Pattern

**Feature File:**
```gherkin
Then search button should be enabled
Then search button should be visible
```

**Step Definition:**
```java
@Then("search button should be enabled")
public void search_button_should_be_enabled() {
    try {
        WebElement searchBtn = driver.findElement(By.name("btnK"));
        assert searchBtn.isEnabled() 
            : "Search button is not enabled";
        System.out.println("✓ Search button is enabled");
    } catch (Exception e) {
        System.out.println("✗ Search button check failed: " + e.getMessage());
    }
}

@Then("search button should be visible")
public void search_button_should_be_visible() {
    try {
        WebElement searchBtn = driver.findElement(By.name("btnK"));
        assert searchBtn.isDisplayed() 
            : "Search button is not visible";
        System.out.println("✓ Search button is visible");
    } catch (Exception e) {
        System.out.println("✗ Search button not found: " + e.getMessage());
    }
}
```

**Key Points:**
- isDisplayed() - Check if visible
- isEnabled() - Check if interactive
- Both return boolean values

---

### 8. Text Content Verification Pattern

**Feature File:**
```gherkin
Then page should contain the text "Google"
Then search button should have text "Search"
```

**Step Definition:**
```java
@Then("page should contain the text {string}")
public void page_should_contain_the_text(String text) {
    String pageSource = driver.getPageSource();
    assert pageSource.contains(text) 
        : "Page does not contain text: " + text;
    System.out.println("✓ Page contains: " + text);
}

@Then("search button should have text {string}")
public void search_button_should_have_text(String text) {
    try {
        WebElement searchBtn = driver.findElement(By.name("btnK"));
        String btnValue = searchBtn.getAttribute("value");
        assert btnValue.contains(text) 
            : "Button text mismatch. Expected: " + text + ", Got: " + btnValue;
        System.out.println("✓ Button has text: " + text);
    } catch (Exception e) {
        System.out.println("✗ Button text verification failed: " + e.getMessage());
    }
}
```

**Key Points:**
- Use driver.getPageSource() for page content
- Use getAttribute() for element attributes
- Verify both page-level and element-level text

---

### 9. Attribute Verification Pattern

**Feature File:**
```gherkin
Then search input field should have placeholder text "Search"
```

**Step Definition:**
```java
@Then("search input field should have placeholder text {string}")
public void search_input_field_should_have_placeholder_text(String placeholder) {
    try {
        WebElement searchBox = driver.findElement(By.name("q"));
        String placeholderText = searchBox.getAttribute("placeholder");
        assert placeholderText.contains(placeholder) 
            : "Placeholder text mismatch. Expected: " + placeholder + ", Got: " + placeholderText;
        System.out.println("✓ Placeholder: " + placeholder);
    } catch (Exception e) {
        System.out.println("✗ Placeholder verification failed: " + e.getMessage());
    }
}
```

**Key Points:**
- Use getAttribute() for HTML attributes
- Common attributes: placeholder, value, type, class, id
- Verify attribute presence and content

---

### 10. Form Input Verification Pattern

**Feature File:**
```gherkin
Then search input field should contain "New search"
```

**Step Definition:**
```java
@Then("search input field should contain {string}")
public void search_input_field_should_contain(String expectedText) {
    try {
        WebElement searchBox = driver.findElement(By.name("q"));
        String actualText = searchBox.getAttribute("value");
        assert actualText.equals(expectedText) 
            : "Field text mismatch. Expected: " + expectedText + ", Got: " + actualText;
        System.out.println("✓ Field contains: " + expectedText);
    } catch (Exception e) {
        System.out.println("✗ Field verification failed: " + e.getMessage());
    }
}
```

**Key Points:**
- Use getAttribute("value") to get input field content
- Use .equals() for exact text match
- Include both expected and actual values in error

---

### 11. Wait for Element Pattern

**Feature File:**
```gherkin
Then search results should be displayed
```

**Step Definition:**
```java
@Then("search results should be displayed")
public void search_results_should_be_displayed() {
    try {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.presenceOfElementLocated(By.id("search")));
        System.out.println("✓ Search results displayed");
    } catch (TimeoutException e) {
        System.out.println("✗ Search results not found within timeout: " + e.getMessage());
    }
}
```

**Key Points:**
- Use WebDriverWait for explicit waits
- presenceOfElementLocated() waits for element to exist in DOM
- 10 seconds is a reasonable timeout
- Handle TimeoutException explicitly

---

### 12. Performance Testing Pattern

**Feature File:**
```gherkin
Then page should load successfully
Then page load time should be less than 10 seconds
```

**Step Definition:**
```java
private long startTime;

@Given("user launches the browser")
public void user_launches_the_browser() {
    // ... browser setup ...
    startTime = System.currentTimeMillis();
}

@Then("page should load successfully")
public void page_should_load_successfully() {
    try {
        String readyState = (String) ((org.openqa.selenium.JavascriptExecutor) driver)
            .executeScript("return document.readyState");
        assert readyState.equals("complete") 
            : "Page not fully loaded";
        System.out.println("✓ Page loaded successfully");
    } catch (Exception e) {
        System.out.println("✗ Page load verification failed: " + e.getMessage());
    }
}

@Then("page load time should be less than {int} seconds")
public void page_load_time_should_be_less_than(int seconds) {
    long endTime = System.currentTimeMillis();
    long loadTime = (endTime - startTime) / 1000;
    assert loadTime < seconds 
        : "Page load time exceeds " + seconds + " seconds. Actual: " + loadTime;
    System.out.println("✓ Page loaded in " + loadTime + " seconds");
}
```

**Key Points:**
- Track start time at browser launch
- Use JavaScript to check document.readyState
- Calculate load time in seconds
- Include actual time in assertion message

---

## 🎯 Best Practices Summary

### 1. Error Handling
```java
try {
    // Action
} catch (Exception e) {
    System.out.println("✗ Error: " + e.getMessage());
}
```

### 2. Logging
```java
System.out.println("✓ Success message");
System.out.println("✗ Error message");
```

### 3. Assertions
```java
assert condition : "Descriptive error message";
```

### 4. Parameterization
```java
@When("user searches for {string}")
public void user_searches_for(String searchTerm) {
    // Use searchTerm parameter
}
```

### 5. Wait Strategies
```java
// Explicit wait (preferred)
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
wait.until(ExpectedConditions.presenceOfElementLocated(By.id("element")));

// Implicit wait (use cautiously)
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));

// Thread sleep (last resort)
Thread.sleep(2000);
```

### 6. Element Location
```java
// By name (most reliable for Google)
By.name("q")

// By ID
By.id("hplogo")

// By class name
By.className("someClass")

// By CSS selector
By.cssSelector("input[name='q']")

// By XPath (least reliable)
By.xpath("//input[@name='q']")
```

---

## 💡 Common Mistakes to Avoid

### ❌ Mistake 1: Not Handling Exceptions
```java
// Bad
WebElement element = driver.findElement(By.id("unknown"));

// Good
try {
    WebElement element = driver.findElement(By.id("unknown"));
} catch (NoSuchElementException e) {
    System.out.println("✗ Element not found: " + e.getMessage());
}
```

### ❌ Mistake 2: Missing Waits
```java
// Bad
driver.get("url");
driver.findElement(By.id("element"));  // Element might not be ready

// Good
driver.get("url");
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
wait.until(ExpectedConditions.presenceOfElementLocated(By.id("element")));
```

### ❌ Mistake 3: Vague Assertion Messages
```java
// Bad
assert title.equals("Google");

// Good
assert title.equals("Google") 
    : "Title mismatch. Expected: Google, Got: " + title;
```

### ❌ Mistake 4: Hardcoded Waits
```java
// Bad
Thread.sleep(5000);  // Always wait 5 seconds

// Good
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
wait.until(ExpectedConditions.elementToBeClickable(By.name("button")));
```

---

## ✅ Checklist for Writing Good Steps

- [ ] Step has clear, descriptive name
- [ ] Step includes try-catch for error handling
- [ ] Step has logging (success and error)
- [ ] Step uses proper waits (WebDriverWait)
- [ ] Step includes descriptive assertions
- [ ] Step uses meaningful locators
- [ ] Step handles timeouts gracefully
- [ ] Step is reusable across scenarios
- [ ] Step is not too complex
- [ ] Step is well-commented

---

**Happy Step Definition Writing! 🚀**
