package com.selenium;

import org.junit.runner.RunWith;
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {
        "com.selenium.steps"
    },
    plugin = {
        "pretty",
        "html:target/cucumber-reports-junit.html",
        "json:target/cucumber-junit.json",
        "junit:target/cucumber-junit-report.xml"
    }
)
public class RunCucumberTest {
    // empty - Cucumber will run the feature files
    // Uses ONE comprehensive StepDefinitions.java from com.selenium.steps
    // Driver lifecycle managed by DriverManager (Singleton pattern)
}
