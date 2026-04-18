Feature: Element Verification and Assertions
  As a QA engineer
  I want to verify element properties
  So that I can ensure the UI is displaying correctly

  Scenario: Verify element visibility
    Given user launches the browser
    When user opens the google website
    Then Wikipedia logo should be visible
    And search input field should be displayed
    And search button should be visible

  Scenario: Verify text content
    Given user launches the browser
    When user opens the google website
    Then page should contain the text "Wikipedia"
    And page should contain the text "Search"

  Scenario: Verify element attributes
    Given user launches the browser
    When user opens the google website
    Then search input field should be visible
    And search button should be visible

  Scenario: Verify page load
    Given user launches the browser
    When user opens the google website
    Then page should load successfully
    And page load time should be less than 20 seconds
