Narrative:
In order to maintain user information
As a user
I want to manage my profile

Scenario: Update profile
Given I am logged in
When I update my profile information
Then my changes should be saved

Scenario: View profile
Given I am logged in
When I view my profile
Then I should see my information
