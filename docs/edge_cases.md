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
