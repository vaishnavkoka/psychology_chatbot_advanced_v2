Feature: Payment Processing and Checkout
  """
  PaymentFeature describes the payment processing workflows
  for e-commerce orders, including validation and error handling.
  """
Background:
  Given the user is on the checkout page

Scenario: Charge valid credit card successfully
  When the user enters valid credit card details, CVV, expiry date and clicks Process Payment
  Then the payment should be processed successfully
  And the order should be created with status "completed"
  And confirmation email should be sent to user

Scenario: Reject payment with invalid card number
  When the user enters invalid card number "1111111111111111" with any CVV and clicks payment
  Then the payment should be rejected
  And error message should display "Invalid card number"
  And the order should not be created

Scenario: Handle declined card from issuer
  When the user enters a card flagged as declined and clicks Process Payment
  Then the payment should be declined by issuer
  And error message should display "Card declined"
  And user should see retry option

Scenario: Apply discount code successfully
  When the user enters discount code "SAVE20" and the system validates the code
  Then discount should be applied
  And the total should be reduced to $80
  And savings amount should display "$20"

Scenario: Reject invalid discount code
  When the user enters invalid discount code "INVALID123" and the system validates the code
  Then discount code should be rejected
  And error message should display "Code not found or expired"
  And cart total should remain unchanged
