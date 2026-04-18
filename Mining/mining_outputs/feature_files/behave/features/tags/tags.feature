Feature: Tagging scenarios
  
  @smoke @critical
  Scenario: Important test
    Given something important
    When I test it
    Then it should pass

  @skip
  Scenario: Skipped test
    Given this is marked to skip
    When run
    Then it should be skipped
