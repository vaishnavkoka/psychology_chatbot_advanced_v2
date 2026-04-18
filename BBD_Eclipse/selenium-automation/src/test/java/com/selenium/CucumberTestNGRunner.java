package com.selenium;

import io.cucumber.testng.AbstractTestNGCucumberTests;
import io.cucumber.testng.CucumberOptions;
import org.testng.annotations.DataProvider;
import org.testng.annotations.AfterSuite;
import com.selenium.utils.DriverManager;

@CucumberOptions(
    features = "src/test/resources/features",
    glue = {
        "com.selenium.steps"
    },
    plugin = {
        "pretty",
        "html:target/cucumber-reports.html",
        "json:target/cucumber.json",
        "junit:target/cucumber-junit.xml"
    }
)
public class CucumberTestNGRunner extends AbstractTestNGCucumberTests {
    
    @Override
    @DataProvider(parallel = false)
    public Object[][] scenarios() {
        return super.scenarios();
    }
    
    /**
     * Close WebDriver after all tests are complete
     * This ensures only ONE Chrome instance was used throughout all tests
     */
    @AfterSuite
    public void tearDownSuite() {
        System.out.println("\n╔════════════════════════════════════════════╗");
        System.out.println("║  All Tests Completed - Closing Driver     ║");
        System.out.println("╚════════════════════════════════════════════╝\n");
        DriverManager.closeDriver();
    }
}
