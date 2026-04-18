# Selenium Cucumber Automation

This project contains a simple Cucumber feature (`src/test/resources/features/google.feature`) with automated test execution.

## ✅ Setup Complete

All required components have been set up and tested:
- ✅ Cucumber dependencies (cucumber-java, cucumber-testng, cucumber-junit) in `pom.xml`
- ✅ TestNG-based Cucumber runner: `CucumberTestNGRunner.java` (recommended; integrates with your TestNG setup)
- ✅ JUnit-based Cucumber runner: `RunCucumberTest.java` (alternative; for pure JUnit execution)
- ✅ Cucumber step definitions: `com.selenium.steps.StepDefinitions.java`
  - Launches Chrome (via WebDriverManager)
  - Opens Google, prints page title, and quits
  - Automatically enables headless Chrome when DISPLAY is missing (CI-friendly)
- ✅ SLF4J Simple binding to eliminate logging warnings
- ✅ Maven Wrapper (mvnw / mvnw.cmd) - no Maven installation needed!
- ✅ **Tests successfully running** ✨

## How to run

### Option 1: Using Maven Wrapper (recommended - no Maven installation needed)

From the project root:

```sh
# Run with TestNG runner (recommended - integrates with existing TestNG setup)
./mvnw clean test -Dtest=CucumberTestNGRunner

# Or run with JUnit runner (alternative)
./mvnw clean test -Dtest=RunCucumberTest

# Or run all tests (TestNG, Cucumber, etc.)
./mvnw test
```

On Windows, use `mvnw.cmd` instead:

```cmd
mvnw.cmd clean test -Dtest=CucumberTestNGRunner
```

### Option 2: Using Maven directly (if installed)

1. Install Java 17 and Maven (if not already installed).
   - Ubuntu/Debian example:

```sh
sudo apt update
sudo apt install openjdk-17-jdk maven -y
```

2. Ensure Google Chrome is installed. On Ubuntu/Debian:

```sh
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

3. From the project root, run:

```sh
# Run with TestNG runner (recommended)
mvn clean test -Dtest=CucumberTestNGRunner

# Or run with JUnit runner (alternative)
mvn clean test -Dtest=RunCucumberTest

# Or run all tests
mvn test
```

## Architecture

- **Feature File**: `src/test/resources/features/google.feature` - Gherkin syntax feature defining the test scenario
- **Step Definitions**: `src/test/java/com/selenium/steps/StepDefinitions.java` - Java implementation of Given/When/Then steps
- **Runners**:
  - `CucumberTestNGRunner.java` - Extends `AbstractTestNGCucumberTests` (recommended; integrates with Maven Surefire TestNG provider)
  - `RunCucumberTest.java` - Uses JUnit runner (alternative; requires explicit `-Dtest=RunCucumberTest`)

## Test Execution Flow

1. Maven/Surefire detects and runs the Cucumber test runner
2. Cucumber parses the feature file and matches steps to step definitions
3. WebDriverManager automatically downloads the appropriate Chromedriver
4. Chrome launches (headless by default in CI/no-DISPLAY environments)
5. Browser navigates to Google, page title is printed, and browser closes
6. Test report generated

## Troubleshooting

- **Chrome not found**: WebDriverManager automatically downloads matching chromedriver, but you must have Chrome/Chromium browser installed
- **Headless mode**: Step definitions enable headless mode automatically when DISPLAY is missing or CI env var is set. To run non-headless locally, ensure DISPLAY is set or modify `StepDefinitions.java`
- **Network issues**: If WebDriverManager cannot download chromedriver due to network restrictions, download a matching version and set: `mvn -Dwebdriver.chrome.driver=/path/to/chromedriver test`
- **CI/Docker environments**: Headless mode is enabled automatically; no additional configuration needed

## Test Verification

The test successfully executes and prints the Google homepage title to the console:
```
Scenario: Open Google and verify title
  Given user launches the browser
  When user opens the google website
  Google
  Then page title should be printed in console
```
