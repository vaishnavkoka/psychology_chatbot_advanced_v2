Narrative:
In order to stay informed
As a user
I want to receive notifications

Scenario: Receive notification
Given notifications are enabled
When an event occurs
Then I should receive a notification

Scenario: Clear notifications
Given I have unread notifications
When I clear them
Then they should be marked as read
