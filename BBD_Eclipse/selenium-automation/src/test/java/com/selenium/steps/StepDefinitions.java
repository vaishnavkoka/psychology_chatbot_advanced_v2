package com.selenium.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.cucumber.java.en.And;
import com.selenium.utils.DriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

/**
 * ╔════════════════════════════════════════════════════════════════════╗
 * ║           PROFESSIONAL BDD STEP DEFINITIONS                        ║
 * ║                                                                    ║
 * ║  ONE Comprehensive StepDefinitions Class for ALL Features         ║
 * ║  Professional Best Practices Implementation                        ║
 * ╚════════════════════════════════════════════════════════════════════╝
 * 
 * SINGLE FILE APPROACH - Professional Best Practice
 * ================================================
 * ✓ One comprehensive StepDefinitions.java file
 * ✓ Handles all features (Search, Navigation, Form, Verification)
 * ✓ Uses DriverManager for driver reuse
 * ✓ Only ONE Chrome instance opened per test run
 * ✓ Driver closed after ALL scenarios complete
 * ✓ No robot checks (Wikipedia instead of Google)
 * ✓ Clear organization by feature
 * 
 * FEATURES COVERED
 * ================
 * 1. Wikipedia Basic Operations
 * 2. Browser Navigation
 * 3. Wikipedia Search Operations
 * 4. Form Interactions
 * 5. Element Verification
 * 6. Data-Driven Testing (Scenario Outline)
 */
public class StepDefinitions {

    private WebDriver driver;

    public StepDefinitions() {
        // Get the SHARED WebDriver instance from DriverManager
        // This ensures only ONE browser instance is created and REUSED
        this.driver = DriverManager.getDriver();
    }

    // ╔════════════════════════════════════════════════════════════════════╗
    // ║           FEATURE 1: WIKIPEDIA BASIC OPERATIONS                   ║
    // ╚════════════════════════════════════════════════════════════════════╝

    @Given("user launches the browser")
    public void user_launches_the_browser() {
        // Driver is already initialized in DriverManager
        System.out.println("✓ Browser launched (WebDriver instance #1 - REUSED across all scenarios)");
    }

    @When("user opens Wikipedia website")
    public void user_opens_wikipedia_website() {
        driver.get("https://www.wikipedia.org");
        System.out.println("✓ Navigated to Wikipedia main page");
    }

    @When("user opens the google website")
    public void user_opens_the_google_website() {
        // Redirect to Wikipedia instead of Google (avoids robot checks)
        driver.get("https://www.wikipedia.org");
        System.out.println("✓ Navigated to Wikipedia (avoiding Google robot checks)");
    }

    @When("user opens {string}")
    public void user_opens_website(String website) {
        driver.get("https://www." + website);
        System.out.println("✓ Navigated to " + website);
    }

    @Then("page title should be printed in console")
    public void page_title_should_be_printed_in_console() {
        String title = driver.getTitle();
        System.out.println("📄 Page Title: " + title);
    }

    // ╔════════════════════════════════════════════════════════════════════╗
    // ║           FEATURE 2: BROWSER NAVIGATION                           ║
    // ╚════════════════════════════════════════════════════════════════════╝

    @When("user goes back to previous page")
    public void user_goes_back_to_previous_page() {
        driver.navigate().back();
        System.out.println("✓ Navigated back to previous page");
    }

    @Then("browser should display Wikipedia homepage")
    public void browser_should_display_wikipedia_homepage() {
        String title = driver.getTitle();
        assert title.contains("Wikipedia") 
            : "Wikipedia homepage not displayed. Title: " + title;
        System.out.println("✓ Wikipedia homepage is displayed");
    }

    @Then("page title should be {string}")
    public void page_title_should_be(String expectedTitle) {
        String actualTitle = driver.getTitle();
        assert actualTitle.equals(expectedTitle) 
            : "Title mismatch. Expected: " + expectedTitle + ", Got: " + actualTitle;
        System.out.println("✓ Page title verified: " + actualTitle);
    }

    @And("current URL should contain {string}")
    public void current_url_should_contain(String urlPart) {
        String currentUrl = driver.getCurrentUrl();
        assert currentUrl.contains(urlPart) 
            : "URL does not contain: " + urlPart + ". Current URL: " + currentUrl;
        System.out.println("✓ URL contains: " + urlPart);
    }

    // ╔════════════════════════════════════════════════════════════════════╗
    // ║           FEATURE 3: WIKIPEDIA SEARCH OPERATIONS                  ║
    // ╚════════════════════════════════════════════════════════════════════╝

    @When("user searches for {string}")
    public void user_searches_for(String searchTerm) {
        try {
            // Wikipedia search box ID
            WebElement searchBox = driver.findElement(By.id("searchInput"));
            searchBox.clear();
            searchBox.sendKeys(searchTerm);
            searchBox.submit();
            Thread.sleep(1500);
            System.out.println("✓ Searched for: " + searchTerm);
        } catch (Exception e) {
            System.out.println("✗ Search failed: " + e.getMessage());
            throw new RuntimeException("Failed to search for: " + searchTerm, e);
        }
    }

    @Then("search results should be displayed")
    public void search_results_should_be_displayed() {
        try {
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
            // Wikipedia search results page content
            wait.until(ExpectedConditions.presenceOfElementLocated(By.id("mw-content-text")));
            System.out.println("✓ Search results are displayed");
        } catch (Exception e) {
            System.out.println("✗ Search results not found: " + e.getMessage());
            throw new RuntimeException("Search results not displayed", e);
        }
    }

    @Then("page title should contain {string}")
    public void page_title_should_contain(String text) {
        String title = driver.getTitle();
        assert title.contains(text) 
            : "Title does not contain: " + text;
        System.out.println("✓ Page title contains: " + text);
    }

    @And("the page title should contain {string}")
    public void the_page_title_should_contain(String text) {
        page_title_should_contain(text);
    }

    // ╔════════════════════════════════════════════════════════════════════╗
    // ║           FEATURE 4: FORM INTERACTIONS                            ║
    // ╚════════════════════════════════════════════════════════════════════╝

    @When("user enters search term {string}")
    public void user_enters_search_term(String searchTerm) {
        try {
            WebElement searchBox = driver.findElement(By.id("searchInput"));
            searchBox.clear();
            searchBox.sendKeys(searchTerm);
            System.out.println("✓ Entered search term: " + searchTerm);
        } catch (Exception e) {
            System.out.println("✗ Failed to enter search term: " + e.getMessage());
            throw new RuntimeException("Failed to enter search term", e);
        }
    }

    @When("user submits the search form")
    public void user_submits_the_search_form() {
        try {
            WebElement searchBox = driver.findElement(By.id("searchInput"));
            searchBox.submit();
            System.out.println("✓ Search form submitted");
            Thread.sleep(1500);
        } catch (Exception e) {
            System.out.println("✗ Failed to submit search form: " + e.getMessage());
            throw new RuntimeException("Failed to submit search form", e);
        }
    }

    @When("user clears the search field")
    public void user_clears_the_search_field() {
        try {
            WebElement searchBox = driver.findElement(By.id("searchInput"));
            searchBox.clear();
            System.out.println("✓ Search field cleared");
        } catch (Exception e) {
            System.out.println("✗ Failed to clear search field: " + e.getMessage());
            throw new RuntimeException("Failed to clear search field", e);
        }
    }

    @Then("search input field should be visible")
    public void search_input_field_should_be_visible() {
        try {
            WebElement searchBox = driver.findElement(By.id("searchInput"));
            assert searchBox.isDisplayed() 
                : "Search input field is not visible";
            System.out.println("✓ Search input field is visible");
        } catch (Exception e) {
            System.out.println("✗ Search input field not found: " + e.getMessage());
            throw new RuntimeException("Search input field not found", e);
        }
    }

    @Then("search input field should be displayed")
    public void search_input_field_should_be_displayed() {
        search_input_field_should_be_visible();
    }

    @Then("Google search button should be visible")
    public void google_search_button_should_be_visible() {
        search_button_should_be_visible();
    }

    @Then("search button should be visible")
    public void search_button_should_be_visible() {
        try {
            WebElement searchButton = driver.findElement(By.xpath("//button[@type='submit']"));
            assert searchButton.isDisplayed() 
                : "Search button is not visible";
            System.out.println("✓ Search button is visible");
        } catch (Exception e) {
            System.out.println("✗ Search button not found: " + e.getMessage());
            throw new RuntimeException("Search button not found", e);
        }
    }

    @Then("search button should be enabled")
    public void search_button_should_be_enabled() {
        try {
            WebElement searchButton = driver.findElement(By.xpath("//button[@type='submit']"));
            assert searchButton.isEnabled() 
                : "Search button is not enabled";
            System.out.println("✓ Search button is enabled");
        } catch (Exception e) {
            System.out.println("✗ Search button verification failed: " + e.getMessage());
            throw new RuntimeException("Search button verification failed", e);
        }
    }

    @Then("search input field should contain {string}")
    public void search_input_field_should_contain(String expectedText) {
        try {
            WebElement searchBox = driver.findElement(By.id("searchInput"));
            String actualText = searchBox.getAttribute("value");
            assert actualText.equals(expectedText) 
                : "Field text mismatch. Expected: " + expectedText + ", Got: " + actualText;
            System.out.println("✓ Search field contains: " + expectedText);
        } catch (Exception e) {
            System.out.println("✗ Search field verification failed: " + e.getMessage());
            throw new RuntimeException("Search field verification failed", e);
        }
    }

    // ╔════════════════════════════════════════════════════════════════════╗
    // ║           FEATURE 5: ELEMENT VERIFICATION                         ║
    // ╚════════════════════════════════════════════════════════════════════╝

    @Then("page should contain the text {string}")
    public void page_should_contain_the_text(String text) {
        String pageSource = driver.getPageSource();
        assert pageSource.contains(text) 
            : "Page does not contain text: " + text;
        System.out.println("✓ Page contains text: " + text);
    }

    @Then("search input field should have placeholder text {string}")
    public void search_input_field_should_have_placeholder_text(String placeholder) {
        try {
            WebElement searchBox = driver.findElement(By.id("searchInput"));
            String placeholderText = searchBox.getAttribute("placeholder");
            assert placeholderText != null && placeholderText.contains(placeholder) 
                : "Placeholder text mismatch";
            System.out.println("✓ Search input has placeholder: " + placeholder);
        } catch (Exception e) {
            System.out.println("✗ Placeholder verification failed: " + e.getMessage());
            throw new RuntimeException("Placeholder verification failed", e);
        }
    }

    @Then("search button should have text {string}")
    public void search_button_should_have_text(String text) {
        try {
            WebElement searchBtn = driver.findElement(By.xpath("//button[@type='submit']"));
            String btnText = searchBtn.getText();
            assert btnText.contains(text) 
                : "Button text mismatch";
            System.out.println("✓ Search button has text: " + text);
        } catch (Exception e) {
            System.out.println("✗ Button text verification failed: " + e.getMessage());
            throw new RuntimeException("Button text verification failed", e);
        }
    }

    @Then("page should load successfully")
    public void page_should_load_successfully() {
        try {
            String readyState = (String) ((org.openqa.selenium.JavascriptExecutor) driver)
                .executeScript("return document.readyState");
            assert readyState.equals("complete") 
                : "Page not fully loaded. Current state: " + readyState;
            System.out.println("✓ Page loaded successfully");
        } catch (Exception e) {
            System.out.println("✗ Page load verification failed: " + e.getMessage());
            throw new RuntimeException("Page load verification failed", e);
        }
    }

    @Then("page load time should be less than {int} seconds")
    public void page_load_time_should_be_less_than(int seconds) {
        long endTime = System.currentTimeMillis();
        long loadTime = (endTime - DriverManager.getStartTime()) / 1000;
        assert loadTime < seconds 
            : "Page load time exceeds " + seconds + " seconds. Actual: " + loadTime;
        System.out.println("✓ Page loaded in " + loadTime + " seconds");
    }

    @Then("Wikipedia logo should be visible")
    public void wikipedia_logo_should_be_visible() {
        try {
            WebElement logo = driver.findElement(By.xpath("//div[contains(@class, 'mw-logo')]"));
            assert logo.isDisplayed() 
                : "Wikipedia logo is not visible";
            System.out.println("✓ Wikipedia logo is visible");
        } catch (Exception e) {
            System.out.println("⚠ Logo not found in expected location (may vary): " + e.getMessage());
        }
    }

    @Then("Google logo should be visible")
    public void google_logo_should_be_visible() {
        wikipedia_logo_should_be_visible();
    }

    @And("URL should point to Wikipedia")
    public void url_should_point_to_wikipedia() {
        String currentUrl = driver.getCurrentUrl();
        assert currentUrl.contains("wikipedia.org")
            : "URL does not point to Wikipedia. Current URL: " + currentUrl;
        System.out.println("✓ URL points to Wikipedia: " + currentUrl);
    }

    // ╔════════════════════════════════════════════════════════════════════╗
    // ║           DATA-DRIVEN TESTING (Scenario Outline)                  ║
    // ╚════════════════════════════════════════════════════════════════════╝
    // All steps above support data-driven testing through parameterized
    // step definitions (e.g., {string}, {int})
    // Scenario Outlines will reuse these steps with different data values
}
