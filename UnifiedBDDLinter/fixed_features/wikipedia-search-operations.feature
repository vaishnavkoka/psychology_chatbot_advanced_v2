Feature: Wikipedia Search Operations
As a user
I want to search on Wikipedia
So that I can find relevant information

Scenario: Search for Selenium
  Given user launches the browser
  When user opens Wikipedia website
  And user searches for "Selenium"
  Then search results should be displayed
  And the application title should contain "Selenium"

Scenario: Search for Cucumber
  Given user launches the browser
  When user opens Wikipedia website
  And user searches for "Cucumber"
  Then search results should be displayed
  And the application title should contain "Cucumber"

Scenario: Multiple searches in one session
  Given user launches the browser
  When user opens Wikipedia website
  And user searches for "Java"
  Then search results should be displayed
  And user searches for "Python"
  Then search results should be displayed
