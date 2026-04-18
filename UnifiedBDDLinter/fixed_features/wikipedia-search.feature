Feature: Wikipedia Search

Scenario: Open Wikipedia and verify title

  Given user launches the browser
  When user opens Wikipedia website
  Then application title should be printed in console
