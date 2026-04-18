package com.selenium.utils;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

/**
 * DriverManager - Manages WebDriver instance (Singleton pattern)
 * Ensures only one Chrome instance is created per test run
 * Driver is reused across all scenarios
 */
public class DriverManager {
    private static WebDriver driver;
    private static long startTime;

    /**
     * Initialize and get WebDriver instance
     * If driver already exists, returns existing instance
     * Otherwise creates a new one
     */
    public static WebDriver getDriver() {
        if (driver == null) {
            initializeDriver();
        }
        return driver;
    }

    /**
     * Initialize Chrome WebDriver with options
     * Handles headless mode for CI/CD environments
     */
    private static void initializeDriver() {
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        
        // Check if running in CI or headless environment
        String display = System.getenv("DISPLAY");
        String ci = System.getenv("CI");
        
        if (ci != null || display == null || display.isEmpty()) {
            options.addArguments("--headless=new");
            options.addArguments("--no-sandbox");
            options.addArguments("--disable-dev-shm-usage");
        }
        
        // Additional options for stability
        options.addArguments("--disable-blink-features=AutomationControlled");
        options.setExperimentalOption("excludeSwitches", new String[]{"enable-automation"});
        options.setExperimentalOption("useAutomationExtension", false);
        
        driver = new ChromeDriver(options);
        driver.manage().window().maximize();
        startTime = System.currentTimeMillis();
        
        System.out.println("✓ Chrome WebDriver initialized (Instance #1)");
    }

    /**
     * Get the start time of driver initialization
     * Useful for performance testing
     */
    public static long getStartTime() {
        return startTime;
    }

    /**
     * Close the WebDriver instance
     * Should be called after all tests are complete
     */
    public static void closeDriver() {
        if (driver != null) {
            driver.quit();
            driver = null;
            System.out.println("✓ Chrome WebDriver closed (after all scenarios)");
        }
    }

    /**
     * Reset driver (for manual cleanup if needed)
     */
    public static void resetDriver() {
        closeDriver();
    }

    /**
     * Check if driver is initialized
     */
    public static boolean isDriverInitialized() {
        return driver != null;
    }
}
