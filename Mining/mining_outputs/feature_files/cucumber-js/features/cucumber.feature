Feature: Running cucumber
  As a developer interested in BDD
  I want to be able to run features with cucumber
  So that I can verify my software works

  Background:
    Given a file named "features/sample.feature" with:
    """
    Feature: Sample
      Scenario: A simple scenario
        Given an empty list
        When I add "item 1"
        Then the list contains "item 1"
    """

  Scenario: Run a simple feature
    When I run cucumber
    Then it should execute 1 scenario
