Feature: Hooks
  
  Scenario: Before hook execution
    Given hooks are defined
    When a scenario starts
    Then before hooks should execute

  Scenario: After hook cleanup
    Given a scenario has run
    When it completes
    Then after hooks should execute
