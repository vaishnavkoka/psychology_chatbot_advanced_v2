Feature: Data-Driven Testing with Examples
  As a QA tester
  I want to test with multiple data inputs
  So that I can verify the application works with different data

  Scenario Outline: Search for different topics
    Given user launches the browser
    When user opens the google website
    And user searches for "<topic>"
    Then search results should be displayed
    And page title should contain "<expected>"

    Examples:
      | topic           | expected        |
      | Automation      | Automation      |
      | Quality         | Quality         |
      | Software        | Software        |
      | Java            | Java            |

  Scenario Outline: Verify URL patterns
    Given user launches the browser
    When user opens "<website>"
    Then current URL should contain "<urlPattern>"

    Examples:
      | website         | urlPattern |
      | wikipedia.org   | wikipedia  |
      | github.com      | github     |
