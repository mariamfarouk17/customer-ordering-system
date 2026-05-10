## Purpose
This document identifies hidden requirements and unusual user behaviors that the Customer Ordering System must handle safely.

The edge cases were discovered by thinking like a frustrated or malicious customer who may enter invalid data, interrupt the ordering process, or try to break the normal system flow.

These cases help ensure that the system is not only working in the normal path, but also protected against invalid inputs, boundary cases, and unexpected user actions.

---

## Persona Discovery

### Persona 1: Frustrated Customer
A customer who repeatedly clicks buttons, refreshes the page, or tries to checkout quickly because they are confused or impatient.

### Persona 2: Malicious Customer
A customer who intentionally sends invalid item IDs, negative quantities, or very large values to test whether the backend accepts bad data.

### Persona 3: Normal Customer with Mistakes
A normal customer who accidentally enters quantity 0, selects an unavailable item, or tries to checkout without noticing that the cart is empty.

---

# Edge Cases

---

## Edge Case 1: Checkout with Empty Cart

### Scenario
The customer clicks the checkout button without adding any items to the cart.

### Risk
The system may create an invalid order with no items, which would cause incorrect order records and confusion for the kitchen or management system.

### Expected Result
The system must reject the checkout request and display a clear error message.

### Error Message
`Your cart is empty. Please add items before checkout.`

### Hidden Requirement
The system shall prevent checkout when the cart contains zero items.

### Related Requirement
Prevent invalid order creation.

### Suggested Test
Given the cart is empty  
When the customer clicks checkout  
Then the system should reject the checkout request and show an empty cart error.

---

## Edge Case 2: Quantity Equals Zero

### Scenario
The customer tries to add a menu item to the cart with quantity equal to 0.

### Risk
The cart may contain meaningless items, and the total price may be calculated incorrectly.

### Expected Result
The system must reject quantity 0 and ask the customer to enter a valid quantity greater than zero.

### Error Message
`Quantity must be at least 1.`

### Hidden Requirement
The system shall only accept item quantities greater than or equal to 1.

### Related Requirement
Validate item quantity before adding items to the cart.

### Suggested Test
Given the customer selects a valid menu item  
When the customer enters quantity 0  
Then the system should reject the request and show a validation error.

---

## Edge Case 3: Negative Quantity

### Scenario
The customer enters a negative quantity such as -1 or -5.

### Risk
A negative quantity may produce a negative total price, which could corrupt order calculations.

### Expected Result
The system must reject negative quantity values.

### Error Message
`Quantity cannot be negative.`

### Hidden Requirement
The system shall prevent negative quantity values from being added to the cart.

### Related Requirement
Prevent invalid cart calculations.

### Suggested Test
Given the customer selects a valid item  
When the customer enters a negative quantity  
Then the system should reject the request.

---

## Edge Case 4: Extremely Large Quantity

### Scenario
The customer enters an extremely large quantity such as 999999.

### Risk
The system may crash, create an unrealistic order, or cause performance and stock handling problems.

### Expected Result
The system must limit the maximum quantity allowed per item.

### Error Message
`Quantity exceeds the maximum allowed limit.`

### Hidden Requirement
The system shall enforce a maximum quantity threshold for each cart item.

### Maximum Allowed Quantity
20 items per menu item.

### Related Requirement
Protect the system from extreme input values.

### Suggested Test
Given the maximum allowed quantity is 20  
When the customer enters quantity 999999  
Then the system should reject the request.

---

## Edge Case 5: Unavailable Menu Item

### Scenario
The customer tries to add an item that is currently unavailable.

### Risk
The system may allow an order that the restaurant cannot prepare.

### Expected Result
The system must prevent unavailable items from being added to the cart and notify the customer.

### Error Message
`This item is currently unavailable.`

### Hidden Requirement
The system shall only allow available menu items to be ordered.

### Related Requirement
Validate item availability before adding it to the cart.

### Suggested Test
Given a menu item is marked as unavailable  
When the customer tries to add it to the cart  
Then the system should reject the request and show an unavailable item message.

---

## Edge Case 6: Invalid Item ID Sent to Backend

### Scenario
The frontend or a malicious user sends an item ID that does not exist in the menu database.

Example:
```json
{
  "item_id": 9999,
  "quantity": 2
}
### Risk
The backend may fail, return incorrect data, or create an order with invalid item information.

### Expected Result
The backend must validate the item ID and reject the request if the item does not exist.

### Error Message
`Invalid item ID.`

### Hidden Requirement
The backend shall validate all item IDs before processing cart or checkout requests.

### Related Requirement
Backend validation must not depend only on frontend validation.

### Suggested Test
Given item ID 9999 does not exist  
When the backend receives a request to add this item  
Then the backend should return a validation error.

---

## Edge Case 7: Double Checkout Click

### Scenario
The customer clicks the checkout button twice quickly.

### Risk
The system may create duplicate orders for the same cart.

### Expected Result
The system must create only one order and prevent duplicate checkout requests.

### Error Message
`Your order is already being processed.`

### Hidden Requirement
The system shall prevent duplicate order submission.

### Related Requirement
Ensure checkout is idempotent or protected from repeated clicks.

### Suggested Test
Given the customer has a valid cart  
When the customer clicks checkout twice quickly  
Then the system should create only one order.

---

## Edge Case 8: Page Refresh During Checkout

### Scenario
The customer refreshes the page while checkout is being processed.

### Risk
The cart may be lost, the order may be duplicated, or the order status may become unclear.

### Expected Result
The system should safely recover by showing either the existing cart or the latest order status.

### Error Message
`Checkout status recovered. Please review your order status.`

### Hidden Requirement
The system shall handle interrupted checkout safely.

### Related Requirement
Maintain consistency during checkout interruptions.

### Suggested Test
Given checkout is in progress  
When the customer refreshes the page  
Then the system should not create duplicate or corrupted orders.

---

## Edge Case 9: Cart Total Calculation Mismatch

### Scenario
The frontend displays a total price that does not match the backend-calculated total.

### Risk
The customer may see an incorrect price, or the system may accept manipulated frontend values.

### Expected Result
The backend must calculate the final total price itself and ignore any total price sent from the frontend.

### Error Message
`Cart total was recalculated by the system.`

### Hidden Requirement
The backend shall be the source of truth for price calculations.

### Related Requirement
Prevent price manipulation and ensure correct total calculation.

### Suggested Test
Given the frontend sends a manipulated total price  
When checkout is submitted  
Then the backend should recalculate the total using stored item prices.

---

## Edge Case 10: Empty or Missing Request Body

### Scenario
The backend receives an empty request body for adding to cart or checkout.

Example:
{
  "item_id": null,
  "quantity": null
}

### Risk
The backend may crash or process incomplete data.

### Expected Result
The backend must reject the request and return a clear validation error.

### Error Message
`Missing required request data.`

### Hidden Requirement
The backend shall validate that all required request fields are present.

### Related Requirement
Validate request format before processing.

### Suggested Test
Given the request body is empty  
When the backend receives the request  
Then the backend should return a validation error.

---

# Summary of Hidden Requirements

| ID | Hidden Requirement | Related Edge Case |
|---|---|---|
| HR1 | The system shall reject checkout when the cart is empty. | Edge Case 1 |
| HR2 | The system shall reject quantity values less than 1. | Edge Case 2, Edge Case 3 |
| HR3 | The system shall enforce a maximum quantity limit. | Edge Case 4 |
| HR4 | The system shall prevent ordering unavailable items. | Edge Case 5 |
| HR5 | The backend shall validate item IDs independently from the frontend. | Edge Case 6 |
| HR6 | The system shall prevent duplicate checkout submissions. | Edge Case 7 |
| HR7 | The system shall recover safely from checkout interruption. | Edge Case 8 |
| HR8 | The backend shall be the source of truth for price calculation. | Edge Case 9 |
| HR9 | The backend shall reject missing or incomplete request data. | Edge Case 10 |

---

# Conclusion

These edge cases improve the reliability of the Customer Ordering System by covering invalid inputs, boundary values, repeated user actions, unavailable items, and backend validation failures.

They also help convert hidden requirements into testable system behaviors, which supports the requirement discovery and validation process.
