package com.selenium.utils;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

public class ScreenshotUtil {

    public static String captureScreenshot(WebDriver driver, String testName) {

        TakesScreenshot ts = (TakesScreenshot) driver;

        File source = ts.getScreenshotAs(OutputType.FILE);

        String destination = "screenshots/" + testName + ".png";

        try {
            Files.createDirectories(Paths.get("screenshots"));
            Files.copy(source.toPath(), Paths.get(destination));
        } catch (IOException e) {
            e.printStackTrace();
        }

        return destination;
    }
}