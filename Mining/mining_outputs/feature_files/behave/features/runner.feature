Feature: Run scenarios
  
  Scenario: Run a single scenario
    Given I have a feature file with a scenario
    When I run behave
    Then the scenario should execute

  Scenario: Run multiple scenarios
    Given multiple feature files exist
    When I run behave
    Then all scenarios should be executed
