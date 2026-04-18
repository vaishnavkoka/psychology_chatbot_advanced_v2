Feature: Step implementations

  Scenario: Define a step
    Given I create a step definition
    When I implement the step
    Then it should be callable

  Scenario Outline: Match step patterns
    Given a pattern "<pattern>"
    When a step matches it with "<args>"
    Then the step should execute with those arguments

    Examples:
      | pattern | args |
      | I have (\d+) items | 5 |
      | I enter "([^"]*)" | hello |
