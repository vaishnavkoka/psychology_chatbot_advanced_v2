Feature: Element Verification and Assertions
As a QA engineer
I want to verify element properties
So that I can ensure the UI is displaying correctly

Scenario: Verify element visibility
  Given user launches the browser
  When user opens the google website
  Then Wikipedia logo should be visible
  And search input input should be displayed
  And search element should be visible

Scenario: Verify text content
  Given user launches the browser
  When user opens the google website
  Then application should contain the content "Wikipedia"
  And application should contain the content "Search"

Scenario: Verify element attributes
  Given user launches the browser
  When user opens the google website
  Then search input input should be visible
  And search element should be visible

Scenario: Verify page load
  Given user launches the browser
  When user opens the google website
  Then application should load successfully
  And application load time should be less than 20 seconds
