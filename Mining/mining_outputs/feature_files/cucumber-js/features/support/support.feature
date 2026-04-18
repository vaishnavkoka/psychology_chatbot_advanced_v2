Feature: Support functions
  
  Scenario: Parse feature files
    Given I have a feature file
    When I parse it
    Then it should have scenarios

  Scenario: Extract step definitions
    Given step definitions exist
    When I load them
    Then all steps should be available
