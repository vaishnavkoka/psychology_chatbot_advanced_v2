package com.selenium.tests;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

import io.github.bonigarcia.wdm.WebDriverManager;

@Listeners(com.selenium.listeners.TestListener.class)

public class FirstTest {

    public WebDriver driver;

    @Test
    public void openGoogle() {

        WebDriverManager.chromedriver().setup();

        driver = new ChromeDriver();

        driver.get("https://www.google.com");
//        assert false; if failed then screenshot is taken
        System.out.println(driver.getTitle());

        driver.quit();
    }
}