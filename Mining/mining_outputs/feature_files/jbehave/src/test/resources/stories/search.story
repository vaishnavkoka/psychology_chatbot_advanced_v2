Narrative:
In order to find information
As a user
I want to search the application

Scenario: Search with results
Given I am on the search page
When I search for "cucumber"
Then I should see at least one result

Scenario: Search with no results
Given I am on the search page
When I search for "xyz123"
Then I should see no results
