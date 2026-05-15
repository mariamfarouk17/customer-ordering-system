Feature: Browse & Search Menu (COS-FR001)

Scenario: View menu grouped by category
Given: the customer opens the menu page
When: the system loads successfully
Then: menu items are displayed grouped by category
And: each item shows name, price, and availability status

Scenario: Search for menu item
Given: the customer is on the menu page
When: the customer searches for "Shawarma"
Then: only matching items are displayed
And: unavailable items are marked as "Unavailable"

Feature: Cart Management (COS-FR002)

Scenario: Add item to cart
Given: the customer selects an available menu item
When: the customer clicks "Add to Cart"
Then: the item is added with quantity 1
And: the cart total is updated

Scenario: Remove item from cart
Given: the cart contains items
When: the customer removes an item
Then: the item is deleted from the cart
And: the total is recalculated

Scenario: Update item quantity
Given: the cart contains an item
When: the customer changes quantity to 3
Then: the cart reflects the new quantity
And: total price is updated

Scenario: Cart persistence after reload
Given: the cart has items
When: the page is refreshed
Then: the cart state remains unchanged

Feature: Order Type Selection (COS-FR003)

Scenario: Select Dine-In order
Given: the customer is on checkout page
When: the customer selects "Dine-In"
And: enters table number
Then: the system saves order type as Dine-In

Scenario: Select Takeaway order
Given: the customer is on checkout page
When: the customer selects "Takeaway"
And: enters pickup time
Then: the system saves order type as Takeaway

Scenario: Missing order type
Given: the customer is on checkout page
When: the customer tries to confirm without selecting order type
Then: an error message is displayed
And: the order is not submitted

Feature: Promo Code (COS-FR004)

Scenario: Apply valid promo code
Given: the cart total is calculated
When: the customer applies a valid promo code
Then: discount is applied correctly

Scenario: Apply invalid promo code
Given: the customer enters a wrong code
When: validation runs
Then: the system shows an error message
And: total remains unchanged

Feature: Payment Processing (COS-FR005)

Scenario: Successful mock payment
Given: the customer confirms checkout
When: payment succeeds
Then: the order is confirmed
And: payment status is saved

Scenario: Failed payment
Given: payment is initiated
When: payment fails
Then: no order is created
And: an error message is shown

Feature: Order Confirmation (COS-FR006)

Scenario: Generate order ID
Given: payment is successful
When: the order is created
Then: the system generates a unique order ID
And: displays confirmation screen

Feature: Order Tracking (COS-FR007)

Scenario: View order status
Given: an order exists
When: the customer opens tracking page
Then: the system shows current status

Feature: Menu Management (COS-FR008)

Scenario: Admin adds new item
Given: admin opens menu panel
When: admin adds new item details
Then: the item appears in customer menu

Scenario: Admin updates item
Given: an item exists
When: admin updates price or availability
Then: changes are reflected in menu
  Then changes are reflected in menu
