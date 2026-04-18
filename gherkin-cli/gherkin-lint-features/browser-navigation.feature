Feature: Browser Navigation
  As a user
  I want to navigate between different websites
  So that I can browse and verify different web pages
Background:
  Given user launches the browser

Scenario: Navigate to Wikipedia homepage
  When user opens the google website
  Then browser should display Wikipedia homepage
  And current URL should contain "wikipedia"

Scenario: Navigate and display Wikipedia page title
  When user opens Wikipedia website
  Then page title should contain "Wikipedia"

Scenario: Go back after navigation
  When user opens Wikipedia website and goes back to previous page
  Then page should load successfully
