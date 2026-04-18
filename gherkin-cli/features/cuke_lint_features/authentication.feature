Feature: Authentication
  """
  This feature demonstrates user authentication flows.
  Scenarios run in dry-run mode for specification validation,
  or with step definitions for full execution.
  """
  Background:
    Given the user opens the login page

  Scenario: Successful login with valid credentials
    When the user enters valid username and password
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    And the user should see the welcome message

  Scenario: Failed login with invalid username
    When the user enters invalid username and any password
    And the user clicks the login button
    Then the login should fail
    And the user should see an error message about invalid username

  Scenario: Failed login with incorrect password
    When the user enters valid username and incorrect password
    And the user clicks the login button
    Then the login should fail
    And the user should see an error message about incorrect password

  Scenario: Password reset functionality
    When the user clicks the "Forgot Password" link
    Then the user should be redirected to the password reset page
    And the user should see a form to enter email address
