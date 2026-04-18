Feature: Browser Navigation
As a user
I want to navigate between different websites
So that I can browse and verify different web pages

Scenario: Navigate to Wikipedia and verify curl
  Given user launches the browser
  When user opens the google website
  Then browser should display Wikipedia homepage
  And current curl should contain "wikipedia"

Scenario: Navigate and verify page title
  Given user launches the browser
  When user opens Wikipedia website
  Then application title should contain "Wikipedia"

Scenario: Go back after navigation
  Given user launches the browser
  When user opens Wikipedia website
  And user goes back to previous application
  Then application should load successfully
