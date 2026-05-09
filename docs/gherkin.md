Feature: Customer Ordering System

# COS-FR001 - Menu Browsing
Scenario: View menu with categories and availability
Given the customer opens the menu page
When the system loads menu data
Then items are displayed grouped by category
And each item shows name, price, and availability status

# COS-FR002 - Cart Management
Scenario: Add item to cart
Given the customer is viewing the menu
When the customer selects an item with quantity between 1 and 10
Then the item is added to the cart
And the cart total is updated correctly

Scenario: Remove item from cart
Given the cart contains at least one item
When the customer removes an item
Then the item is removed from the cart
And the cart total is recalculated

Scenario: Restore cart after page reload
Given the customer has items in the cart
When the page is refreshed
Then the cart state is restored from session storage or server session

# COS-FR003 - Order Type Selection
Scenario: Select order type
Given the customer is ready to checkout
When the customer selects order type as dine-in or takeaway
Then the system records the selection
And requires table number if dine-in is selected

# COS-FR004 - Promo Code Validation
Scenario: Apply valid promo code
Given the customer enters a promo code
When the code is validated
Then the discount is applied to the order total

Scenario: Reject invalid promo code
Given the customer enters an invalid or expired promo code
When validation is performed
Then the system rejects the code
And shows an error message

# COS-FR005 - Payment Processing
Scenario: Successful payment
Given the customer selects a payment method
When payment is processed successfully
Then the order status becomes confirmed
And payment is recorded

Scenario: Failed payment
Given the payment is initiated
When the payment fails
Then the order is not confirmed
And the customer is notified

# COS-FR006 - Order Confirmation
Scenario: Generate order confirmation
Given the payment is successful
When the order is created
Then the system generates a unique order ID
And stores the order in the database

# COS-FR007 - Order Tracking
Scenario: Track order status
Given an order exists
When the customer opens the tracking page
Then the system displays current status (Pending, Confirmed, Cancelled)

# COS-NFR001 - Performance
Scenario: System response time
Given multiple users access the system
When they perform checkout
Then the response time is under 3 seconds
