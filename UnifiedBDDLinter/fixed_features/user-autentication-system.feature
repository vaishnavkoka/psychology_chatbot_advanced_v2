Feature: User authentication System

Scenario: valid Login
  Given user is on log application
  When user provide valid credentials
  Then user is loved in successfully

Scenario: Forgot password
  Given user is on login application
  When user interact with forgot password navigation element
  Then password reset email is sent
