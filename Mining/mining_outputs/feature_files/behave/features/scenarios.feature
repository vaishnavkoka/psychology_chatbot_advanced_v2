Feature: Scenario variations
  
  Scenario: Simple scenario
    Given precondition
    When action
    Then outcome

  Scenario Outline: Data-driven scenario
    Given I have <input>
    When I process it
    Then I get <output>

    Examples:
      | input | output |
      | 1     | 2      |
      | 3     | 4      |
