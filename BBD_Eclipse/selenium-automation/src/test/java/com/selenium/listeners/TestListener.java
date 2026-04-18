package com.selenium.listeners;

import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.selenium.reports.ExtentReportManager;
import org.openqa.selenium.WebDriver;
import com.selenium.utils.ScreenshotUtil;

public class TestListener implements ITestListener {

    ExtentReports extent = ExtentReportManager.getReportInstance();
    ExtentTest test;

    public void onTestStart(ITestResult result) {
        test = extent.createTest(result.getMethod().getMethodName());
    }

    public void onTestSuccess(ITestResult result) {
        test.pass("Test Passed");
    }

    public void onTestFailure(ITestResult result) {

        test.fail(result.getThrowable());

        Object testClass = result.getInstance();
        WebDriver driver = ((com.selenium.tests.FirstTest) testClass).driver;

        String screenshotPath = ScreenshotUtil.captureScreenshot(driver, result.getMethod().getMethodName());

        test.addScreenCaptureFromPath(screenshotPath);
    }

    public void onFinish(ITestContext context) {
        extent.flush();
    }
}