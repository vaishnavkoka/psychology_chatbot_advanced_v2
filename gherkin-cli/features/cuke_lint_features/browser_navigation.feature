Feature: Browser Navigation
  As a user
  I want to navigate between different websites
  So that I can browse and verify different web pages
Background: 
    Given user launches the browser

  Scenario: Navigate to Wikipedia homepage
    # Given user launches the browser
    When user opens the google website
    Then browser should display Wikipedia homepage
    And current URL should contain "wikipedia"

  Scenario: Navigate and display Wikipedia page title
    # Given user launches the browser
    When user opens Wikipedia website
    Then page title should contain "Wikipedia"

  Scenario: Go back after navigation
    # Given user launches the browser
    When user opens Wikipedia website
    And user goes back to previous page
    Then page should load successfully
