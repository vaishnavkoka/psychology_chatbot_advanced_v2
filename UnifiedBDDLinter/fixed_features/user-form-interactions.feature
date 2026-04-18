Feature: User Form Interactions
As a user
I want to interact with web forms
So that I can input data and verify form functionality

Scenario: Fill search form and submit
  Given user launches the browser
  When user opens the google website
  And user provide search term "Selenium WebDriver"
  And user submits the search data entry
  Then search results should be displayed

Scenario: Verify form elements
  Given user launches the browser
  When user opens the google website
  Then search input input should be visible
  And search element should be visible
  And search element should be enabled

Scenario: Clear and re-enter search text
  Given user launches the browser
  When user opens the google website
  And user provide search term "Initial search"
  And user reset the search input
  And user provide search term "New search"
  Then search input input should contain "New search"
