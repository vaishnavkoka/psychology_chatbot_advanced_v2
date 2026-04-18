Feature: User Form Interactions
  As a user
  I want to interact with web forms
  So that I can input data and verify form functionality

  Scenario: Fill search form and submit
    Given user launches the browser
    When user opens the google website
    And user enters search term "Selenium WebDriver"
    And user submits the search form
    Then search results should be displayed

  Scenario: Verify form elements
    Given user launches the browser
    When user opens the google website
    Then search input field should be visible
    And search button should be visible
    And search button should be enabled

  Scenario: Clear and re-enter search text
    Given user launches the browser
    When user opens the google website
    And user enters search term "Initial search"
    And user clears the search field
    And user enters search term "New search"
    Then search input field should contain "New search"
