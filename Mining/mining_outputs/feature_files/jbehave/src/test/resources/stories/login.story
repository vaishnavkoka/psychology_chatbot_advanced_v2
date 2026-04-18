Narrative:
In order to access protected resources
As a user
I want to login to the system

Scenario: Successful login
Given I am on the login page
When I enter valid credentials
Then I should see the dashboard

Scenario: Failed login
Given I am on the login page
When I enter invalid credentials
Then I should see an error message
