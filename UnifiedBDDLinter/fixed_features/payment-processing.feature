Feature: Payment Processing
Test payment functionality

Scenario: Verify payment works
  When I interact with the pay element
  And I wait for 2 seconds
  And I check if the ass selector .payment-modal is visible
  And I navigate to to element path=//*[@id="card-number"]
  And I enter "4111111111111111" in the content input
  And I interact with the confirm element
  And I verify the response son contains success
  And I query the database to verify payment record exists
  And I check and test and do things
  Then everything should work

Scenario: Some test scenario
  Given test data exists
  When I do some action
  Then I verify it

Scenario: Another similar payment scenario
  When I interact with the pay element
  And I enter card number "4111111111111111"
  And I interact with confirm
  Then payment should be processed

Scenario: Edge case scenario
  Given user has no payment method
  When user tries to make payment
  Then system attempts action
  And something gets verified
