Feature: User Authentication
As a user
I want to securely authenticate to the system
So that I can access my account

Scenario: Successfully login with valid credentials
  Given the user is on the login application
  When the user provide valid username and password
  And the user interact with the login element
  Then the user should be redirected to the dashboard
  And the user should see their profile name

Scenario: Display error message for invalid credentials
  Given the user is on the login application
  When the user provide an invalid username
  And the user provide an invalid password
  And the user interact with the login element
  Then the system should display an "Invalid credentials" error
  And the user should remain on the login application

Scenario: Lock account after failed attempts
  Given the user is on the login application
  When the user attempts to login 5 times with wrong password
  Then the account should be locked
  And the user should see a "Account locked" message
  And the user should receive a password reset email
