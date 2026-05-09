# 🍽️ Customer Ordering System (COS)
## Phase 2 — Behavioural & Design Specification

> **Stack:** Python Flask · HTML/CSS/JS · SQLite · Mock Payment  
> **Team:** 3 students 

---

## 📋 Table of Contents

1. [Gherkin Scenarios](#1-gherkin-scenarios)
2. [UML Diagrams — Plain-English Explanation](#2-uml-diagrams--plain-english-explanation)
3. [System Sequence Diagrams](#3-system-sequence-diagrams)
4. [Activity Diagrams](#4-activity-diagrams)
5. [API Contracts](#5-api-contracts)
6. [QA Refinement Loop](#6-qa-refinement-loop)
7. [Information Hiding](#7-information-hiding)

---

## 1. Gherkin Scenarios

> Each scenario maps directly to a requirement from Phase 1.  
> Format: `Feature → Scenario → Given / When / Then`

---

### Feature: Browse & Search Menu (`COS-FR001`)

```gherkin
Feature: Browse and Search Menu

  Scenario: Customer views menu items grouped by category
    Given the customer opens the menu page
    When the page finishes loading
    Then menu items shall be displayed grouped by category
    And each item shall show its name, price, and availability status

  Scenario: Customer searches for a specific item
    Given the customer is on the menu page
    When the customer types "Shawarma" in the search box
    Then only items whose name contains "Shawarma" shall be displayed
    And unavailable items shall be clearly labelled as "Unavailable"
```

---

### Feature: Cart Management (`COS-FR002`)

```gherkin
Feature: Cart Management

  Scenario: Customer adds an item to the cart
    Given the customer is viewing a menu item that is available
    When the customer clicks "Add to Cart"
    Then the item shall appear in the cart with quantity 1
    And the cart total shall update to reflect the item price

  Scenario: Customer removes an item from the cart
    Given the cart contains at least one item
    When the customer clicks "Remove" next to that item
    Then the item shall be removed from the cart
    And the cart total shall decrease accordingly

  Scenario: Customer updates item quantity
    Given the cart contains an item with quantity 1
    When the customer changes the quantity to 3
    Then the cart shall show that item with quantity 3
    And the cart total shall reflect the updated quantity

  Scenario: Cart survives a page reload
    Given the customer has added items to the cart
    When the customer reloads the page
    Then the cart shall still contain the same items
    And the cart total shall remain the same
```

---

### Feature: Order Type Selection (`COS-FR003`)

```gherkin
Feature: Order Type Selection

  Scenario: Customer selects Dine-In
    Given the customer is on the checkout page
    When the customer selects "Dine-In"
    And enters table number "5"
    Then the order shall be tagged as Dine-In with table number 5

  Scenario: Customer selects Takeaway
    Given the customer is on the checkout page
    When the customer selects "Takeaway"
    And enters pick-up time "13:30"
    Then the order shall be tagged as Takeaway with pick-up time 13:30

  Scenario: Customer tries to submit without selecting an order type
    Given the customer is on the checkout page
    When the customer clicks "Confirm Order" without selecting an order type
    Then the system shall display an error: "Please select Dine-In or Takeaway"
    And the order shall not be submitted
```

---

### Feature: Promo Code Application (`COS-FR004`)

```gherkin
Feature: Discount and Promo Code Application

  Scenario: Customer applies a valid promo code
    Given the cart total is £20.00
    And a valid promo code "SAVE10" exists with 10% discount
    When the customer enters "SAVE10" and clicks "Apply"
    Then the discount of £2.00 shall be applied
    And the new cart total shall display as £18.00

  Scenario: Customer applies an expired promo code
    Given the promo code "SUMMER21" has an expiry date in the past
    When the customer enters "SUMMER21" and clicks "Apply"
    Then the system shall display: "This promo code has expired"
    And no discount shall be applied

  Scenario: Customer applies an invalid promo code
    Given the promo code "FAKECODE" does not exist in the system
    When the customer enters "FAKECODE" and clicks "Apply"
    Then the system shall display: "Invalid promo code"
    And no discount shall be applied

  Scenario: Customer applies a second promo code
    Given the customer has already applied promo code "SAVE10"
    When the customer tries to enter a second promo code "DEAL5"
    Then the system shall display: "Only one promo code is allowed per order"
    And the second code shall not be applied
```

---

### Feature: Payment Processing (`COS-FR005`)

```gherkin
Feature: Simulated Payment Processing

  Scenario: Customer pays successfully with Mock Card
    Given the cart contains items and an order type is selected
    When the customer selects "Mock Card" and clicks "Pay"
    Then the payment simulator shall return a success response
    And the system shall proceed to generate an order confirmation

  Scenario: Customer pays with Cash
    Given the cart contains items and an order type is selected
    When the customer selects "Cash" and clicks "Pay"
    Then the order shall be confirmed with payment method "Cash"
    And a confirmation screen shall be displayed

  Scenario: Payment simulation returns failure
    Given the customer selects "Mock Card" (set to fail mode for testing)
    When the customer clicks "Pay"
    Then the payment simulator shall return a failure response
    And the system shall display: "Payment failed. Please try again."
    And no order shall be created
```

---

### Feature: Order Confirmation (`COS-FR006`)

```gherkin
Feature: Order Confirmation and Receipt

  Scenario: System generates order confirmation after successful payment
    Given the payment has succeeded
    When the system processes the order
    Then a unique Order ID shall be generated (e.g., ORD-00042)
    And a confirmation screen shall display the Order ID and items ordered

  Scenario: Order is saved to the database
    Given the order confirmation has been generated
    When the order is confirmed
    Then the order details (items, total, order type, status) shall be saved in the database
```

---

### Feature: Order Status Tracking (`COS-FR007`)

```gherkin
Feature: Live Order Status Tracking

  Scenario: Customer views their order status
    Given the customer has a confirmed order with ID "ORD-00042"
    When the customer navigates to the order status page
    Then the system shall display the current status as "Pending", "Confirmed", or "Cancelled"

  Scenario: Staff updates order status to Confirmed
    Given an order exists with status "Pending"
    When the cashier updates the status to "Confirmed"
    Then the order status page shall show "Confirmed"
```

---

### Feature: Menu Management (`COS-FR008`)

```gherkin
Feature: Menu and Inventory Management

  Scenario: Admin adds a new menu item
    Given the admin is on the menu management page
    When the admin enters item name "Falafel Wrap", price "£5.50", and category "Wraps"
    And clicks "Save"
    Then the new item shall appear on the customer menu page

  Scenario: Admin marks an item as unavailable
    Given a menu item "Chicken Shawarma" is currently available
    When the admin toggles the item to "Unavailable"
    Then the item shall appear as unavailable on the customer menu
    And customers shall not be able to add it to the cart

  Scenario: Admin updates item price
    Given the admin is on the menu management page
    When the admin changes the price of "Falafel Wrap" from £5.50 to £6.00
    And clicks "Save"
    Then the customer menu shall display the updated price of £6.00
```

---

### Feature: Edge Case — Idempotent Checkout (`COS-FR013`)

```gherkin
Feature: Idempotent Checkout

  Scenario: Customer submits payment twice due to slow network
    Given the customer has clicked "Pay" and a payment request was sent
    When the same request is submitted again within 60 seconds with the same idempotency key
    Then the system shall return the original payment result
    And the customer shall not be charged twice
```

---

### Feature: Edge Case — Server-Side Price Validation (`COS-FR014`)

```gherkin
Feature: Server-Side Price Validation

  Scenario: Tampered price is rejected at checkout
    Given a customer has items in the cart with a server price of £10.00
    When a modified request arrives at /api/checkout with total set to £0.01
    Then the server shall reject the order with status 422
    And shall return: "Order total mismatch. Please refresh and try again."
```

---

### Feature: Edge Case — Cart Persistence (`COS-FR015`)

```gherkin
Feature: Resilient Cart Persistence

  Scenario: Cart is restored after connection loss
    Given the customer has added items to the cart
    And the customer loses their internet connection
    When the customer reloads the page
    Then the cart shall be restored from localStorage
    And a banner shall appear: "Your cart has been restored"
```

---

### Feature: Invalid Promo Code Handling (`COS-FR016`)

```gherkin
Feature: Invalid Promo Code Handling

 Scenario: Invalid promo code does not change cart total
    Given the cart total is 100.00
    When the customer enters promo code "FAKECODE"
    Then the system shall display "Invalid promo code"
    And the cart total shall remain 100.00
```

---

### Feature: Edge Case — Stock Validation at Checkout (`COS-FR017`)

```gherkin
Feature: Real-Time Stock Validation at Checkout

  Scenario: An item becomes unavailable between cart addition and checkout
    Given the customer added "Chicken Shawarma" to the cart 10 minutes ago
    And the admin has since marked it as "Unavailable"
    When the customer submits the order
    Then the system shall reject the order
    And display: "Chicken Shawarma is no longer available. Please remove it from your cart."
    And the customer shall not be charged
```

---

## 2. UML Diagrams — Plain-English Explanation

> These are described in plain English so they can be drawn in any tool (draw.io, Lucidchart, pen and paper).

---

### 2.1 Use Case Diagram

**What it shows:** Who does what in the system.

**Actors and their use cases:**

```
Customer
  ├── Browse Menu
  ├── Search Menu
  ├── Add Item to Cart
  ├── Remove Item from Cart
  ├── Select Order Type (Dine-In / Takeaway)
  ├── Apply Promo Code
  ├── Checkout (Pay)
  └── View Order Status

Cashier / Staff
  ├── Create Order on Behalf of Customer
  ├── Modify Existing Order
  └── Mark Item as Unavailable

System Admin
  ├── Add Menu Item
  ├── Update Menu Item
  └── Mark Item as Unavailable

Payment Simulator (Offstage)
  └── Return Payment Success or Failure

Data Storage (Offstage)
  ├── Store Order
  ├── Store Cart
  ├── Retrieve Menu Items
  └── Store/Retrieve Promo Codes
```

**Relationships:**
- `Cashier` can perform everything `Customer` can (uses the `<<extend>>` relationship on "Create Order")
- `Checkout` includes `Payment Processing` (`<<include>>`)
- `Checkout` includes `Stock Validation` (`<<include>>`)

---

### 2.2 Class Diagram

**What it shows:** The data objects (classes) in the system and how they relate.

```
MenuItem
  - id: int
  - name: string
  - price: float
  - category: string
  - is_available: bool

CartItem
  - menu_item_id: int
  - quantity: int
  - unit_price: float

Cart
  - session_id: string
  - items: list[CartItem]
  - promo_code: string (optional)
  - total: float

Order
  - order_id: string  (e.g. ORD-00042)
  - cart: Cart
  - order_type: string  (Dine-In / Takeaway)
  - table_number: int (optional)
  - pickup_time: string (optional)
  - payment_method: string
  - status: string  (Pending / Confirmed / Cancelled)
  - created_at: datetime

PromoCode
  - code: string
  - discount_percent: float
  - expiry_date: date
  - is_active: bool
```

**Relationships:**
- `Cart` contains one or more `CartItem`
- Each `CartItem` references one `MenuItem`
- `Order` is created from a `Cart`
- `Order` may reference one `PromoCode`

---

### 2.3 Component Diagram

**What it shows:** The three main software components and how they communicate.

```
[ Browser (HTML/CSS/JS) ]
        |
        | HTTP requests (fetch / form submit)
        v
[ Flask Backend (Python) ]
        |
        | SQL queries
        v
[ SQLite Database ]
```

- The browser renders pages and sends requests to Flask routes.
- Flask handles business logic (price validation, stock check, order creation).
- SQLite stores all persistent data (menu items, orders, promo codes).
- The Payment Simulator is a Python function inside Flask — no external service needed.

---

## 3. System Sequence Diagrams

> These describe the message flow between the customer (browser), the Flask backend, and the database for the two most important flows.

---

### 3.1 Place Order — Happy Path

```
Customer (Browser)          Flask Backend           SQLite DB
      |                          |                       |
      |-- GET /menu ------------->|                       |
      |                          |-- SELECT menu_items -->|
      |                          |<-- menu rows ----------|
      |<-- render menu page ------|                       |
      |                          |                       |
      |-- POST /cart/add -------->|                       |
      |                          |-- validate item_id --->|
      |                          |<-- item exists --------|
      |<-- cart updated ----------|                       |
      |                          |                       |
      |-- POST /checkout -------->|                       |
      |   (order_type,            |                       |
      |  payment_method)         |                        |
      |                          |-- re-fetch prices ---->|
      |                          |<-- authoritative totl--|
      |                          |-- check stock -------->|
      |                          |<-- all available ------|
      |                          |-- call PaySimulator()  |
      |                          |<-- {status: "success"} |
      |                          |-- INSERT order ------->|
      |                          |<-- order saved --------|
      |<-- 200 {order_id: ORD-42}|                       |
      |                          |                       |
      |-- GET /order/ORD-42 ----->|                       |
      |                          |-- SELECT order ------->|
      |                          |<-- order row ----------|
      |<-- render status: Pending|                       |
```

---

### 3.2 Place Order — Payment Failure Path

```
Customer (Browser)          Flask Backend           SQLite DB
      |                          |                       |
      |-- POST /checkout -------->|                       |
      |                          |-- re-fetch prices ---->|
      |                          |<-- totals match -------|
      |                          |-- check stock -------->|
      |                          |<-- all available ------|
      |                          |-- call PaySimulator()  |
      |                          |<-- {status: "failure"} |
      |                          |   (no INSERT)          |
      |<-- 402 {error: "Payment  |                       |
      |    failed. Try again."} --|                       |
```

---

### 3.3 Admin Updates Menu Item

```
Admin (Browser)             Flask Backend           SQLite DB
      |                          |                       |
      |-- GET /admin/menu ------->|                       |
      |                          |-- SELECT menu_items -->|
      |                          |<-- all items ----------|
      |<-- render admin page -----|                       |
      |                          |                       |
      |-- POST /admin/menu/update>|                       |
      |   (item_id, price,        |                       |
      |    is_available)          |                       |
      |                          |-- UPDATE menu_item --->|
      |                          |<-- updated OK ---------|
      |<-- 200 {message: "Saved"} |                       |
```

---

## 4. Activity Diagrams

> These describe the step-by-step logic flow for key processes. Draw these as flowcharts with decision diamonds.

---

### 4.1 Customer Places an Order

```
START
  |
  v
[Open Menu Page]
  |
  v
[Browse / Search Items]
  |
  v
[Add Items to Cart]
  |
  v
[Apply Promo Code?]
  |-- YES --> [Validate Code] --> [Valid?]
  |                                  |-- YES --> [Apply Discount]
  |                                  |-- NO  --> [Show Error] --> loop back
  |-- NO  --> (continue)
  |
  v
[Select Order Type: Dine-In or Takeaway]
  |
  v
[Enter Table Number OR Pick-up Time]
  |
  v
[Click "Pay" — Select Cash or Mock Card]
  |
  v
[Backend: Re-validate prices & stock]
  |
  v
[Prices match & all items available?]
  |-- NO  --> [Show Error to Customer] --> END
  |-- YES --> (continue)
  |
  v
[Run Payment Simulator]
  |
  v
[Payment Successful?]
  |-- NO  --> [Show "Payment Failed"] --> END
  |-- YES --> (continue)
  |
  v
[Generate Order ID]
  |
  v
[Save Order to Database]
  |
  v
[Show Confirmation Screen with Order ID]
  |
  v
END
```

---

### 4.2 Admin Manages Menu

```
START
  |
  v
[Admin Logs In / Opens Admin Page]
  |
  v
[View All Menu Items]
  |
  v
[Action?]
  |-- ADD     --> [Fill in Name, Price, Category] --> [Save] --> [INSERT to DB]
  |-- UPDATE  --> [Edit Price or Availability]    --> [Save] --> [UPDATE in DB]
  |-- DISABLE --> [Toggle item to Unavailable]    --> [Save] --> [UPDATE is_available=false]
  |
  v
[Changes reflected on customer menu within page refresh]
  |
  v
END
```

---

### 4.3 Edge Case — Stock Validation at Checkout

```
START (checkout submitted)
  |
  v
[For each item in cart]
  |
  v
[Query database: is item still available?]
  |
  v
[All items available?]
  |-- NO  --> [Return list of unavailable items]
  |           [Show error: "X is no longer available"]
  |           [Do NOT charge customer]
  |           END
  |-- YES --> [Continue to payment]
  |
  v
END (proceed normally)
```

---

## 5. API Contracts

> All endpoints are simple Flask routes. Request and response bodies are JSON.  
> Base URL: `http://localhost:5000`

---

### 5.1 GET `/api/menu`

**Description:** Returns all menu items grouped by category.  
**Actor:** Customer, Admin  

**Response `200 OK`:**
```json
{
  "categories": [
    {
      "name": "Wraps",
      "items": [
        {
          "id": 1,
          "name": "Chicken Shawarma",
          "price": 6.50,
          "is_available": true
        },
        {
          "id": 2,
          "name": "Falafel Wrap",
          "price": 5.50,
          "is_available": false
        }
      ]
    }
  ]
}
```

---

### 5.2 POST `/api/cart/add`

**Description:** Adds one item to the session cart.  
**Actor:** Customer  

**Request Body:**
```json
{
  "item_id": 1,
  "quantity": 2
}
```

**Response `200 OK`:**
```json
{
  "cart_total": 13.00,
  "items": [
    { "item_id": 1, "name": "Chicken Shawarma", "quantity": 2, "unit_price": 6.50 }
  ]
}
```

**Response `400 Bad Request` (item unavailable):**
```json
{ "error": "This item is currently unavailable." }
```

---

### 5.3 POST `/api/cart/remove`

**Description:** Removes an item from the session cart.  
**Actor:** Customer  

**Request Body:**
```json
{ "item_id": 1 }
```

**Response `200 OK`:**
```json
{
  "cart_total": 0.00,
  "items": []
}
```

---

### 5.4 POST `/api/promo/apply`

**Description:** Validates and applies a promo code to the cart.  
**Actor:** Customer  

**Request Body:**
```json
{ "code": "SAVE10" }
```

**Response `200 OK`:**
```json
{
  "discount_percent": 10,
  "discount_amount": 1.30,
  "new_total": 11.70
}
```

**Response `400 Bad Request`:**
```json
{ "error": "Invalid promo code." }
```

**Response `400 Bad Request` (expired):**
```json
{ "error": "This promo code has expired." }
```

---

### 5.5 POST `/api/checkout`

**Description:** Validates the order, runs the payment simulator, and creates the order.  
**Actor:** Customer  

**Request Body:**
```json
{
  "order_type": "Dine-In",
  "table_number": 5,
  "payment_method": "Mock Card"
}
```

**Response `200 OK`:**
```json
{
  "order_id": "ORD-00042",
  "status": "Pending",
  "message": "Order placed successfully!"
}
```

**Response `402 Payment Required`:**
```json
{ "error": "Payment failed. Please try again." }
```

**Response `422 Unprocessable Entity` (price mismatch):**
```json
{ "error": "Order total mismatch. Please refresh and try again." }
```

**Response `422 Unprocessable Entity` (item unavailable):**
```json
{
  "error": "Some items are no longer available.",
  "unavailable_items": ["Chicken Shawarma"]
}
```

---

### 5.6 GET `/api/order/<order_id>`

**Description:** Returns the current status of an order.  
**Actor:** Customer  

**Response `200 OK`:**
```json
{
  "order_id": "ORD-00042",
  "status": "Pending",
  "order_type": "Dine-In",
  "table_number": 5,
  "items": [
    { "name": "Chicken Shawarma", "quantity": 2, "unit_price": 6.50 }
  ],
  "total": 13.00,
  "created_at": "2025-05-09T14:30:00"
}
```

**Response `404 Not Found`:**
```json
{ "error": "Order not found." }
```

---

### 5.7 POST `/api/admin/menu`

**Description:** Adds a new menu item.  
**Actor:** System Admin  

**Request Body:**
```json
{
  "name": "Falafel Wrap",
  "price": 5.50,
  "category": "Wraps",
  "is_available": true
}
```

**Response `201 Created`:**
```json
{ "message": "Menu item added.", "item_id": 3 }
```

---

### 5.8 PUT `/api/admin/menu/<item_id>`

**Description:** Updates an existing menu item (price, availability).  
**Actor:** System Admin  

**Request Body:**
```json
{
  "price": 6.00,
  "is_available": false
}
```

**Response `200 OK`:**
```json
{ "message": "Menu item updated." }
```

---

## 6. QA Refinement Loop

> For each requirement, this section defines: what to test, how to test it, and what "done" looks like.

---

### Round 1 — Functional Correctness

| Req ID | What to Test | How to Test | Pass Condition |
|--------|-------------|-------------|----------------|
| `COS-FR001` | Menu loads with correct items and categories | Open browser, load `/menu` | All items visible, grouped, with name/price/status |
| `COS-FR002` | Add, remove, update cart | Click Add/Remove/Qty buttons | Cart total updates correctly each time |
| `COS-FR003` | Order type selection is required | Submit without selecting type | Error message shown; order not created |
| `COS-FR004` | Valid promo applies; invalid/expired rejected | Try 3 codes: valid, expired, fake | Each returns correct message and behaviour |
| `COS-FR005` | Mock payment returns success and failure | Toggle simulator mode | Correct screen shown for each outcome |
| `COS-FR006` | Order ID generated and saved | Complete checkout | Order ID shown on screen; row exists in DB |
| `COS-FR007` | Status page shows correct status | Complete order, check status page | Status reads "Pending" after order created |
| `COS-FR008` | Admin can add/update/disable items | Use admin panel | Changes reflected on customer menu |

---

### Round 2 — Edge Case & Security Checks

| EC ID | What to Test | How to Test | Pass Condition |
|-------|-------------|-------------|----------------|
| `EC-01` | Duplicate checkout click | Click Pay twice quickly | Only one order is created |
| `EC-02` | Tampered price rejected | Send POST `/checkout` with modified total via browser console | HTTP 422 returned; order not created |
| `EC-03` | Cart restored after reload | Add items, clear network, reload page | Cart restored from localStorage; banner shown |
| `EC-04` | Invalid promo code does not change total | Enter invalid promo code | Error shown; cart total remains unchanged |
| `EC-05` | Unavailable item caught at checkout | Add item, disable it via admin, then checkout | HTTP 422 with item name; no charge |

---

### Round 3 — Non-Functional Checks

| NFR ID | What to Measure | How to Measure | Target |
|--------|----------------|----------------|--------|
| `COS-NFR001` | Menu page load time | Chrome DevTools → Network tab | ≤ 2 seconds on throttled 4G |
| `COS-NFR001` | Checkout response time | Time from click to confirmation | ≤ 3 seconds |
| `COS-NFR002` | Server never trusts client total | Check Flask route logic in code review | Price always re-fetched from DB |
| `COS-NFR003` | Invalid inputs handled gracefully | Submit empty form; send bad JSON | No server crash; error message shown |
| `COS-NFR004` | Checkout steps count | Walk through the UI manually | Completed in ≤ 5 clicks/steps |

---

### QA Sign-Off Checklist

```
[ ] All 8 functional requirements have a passing test
[ ] All 5 edge cases have a passing test
[ ] No server crash on bad input (empty fields, wrong types, missing keys)
[ ] Checkout cannot be completed without selecting order type
[ ] Admin changes appear on the customer menu after page refresh
[ ] Payment failure shows an error — no order is saved
[ ] Duplicate Pay clicks do not create multiple orders
[ ] Invalid promo code shows an error and does not change the cart total
```

---

## 7. Information Hiding

> Information Hiding means each module only exposes what others need to know — and hides the rest. This is how we keep the code clean and maintainable in one week.

---

### 7.1 What is Information Hiding?

Information hiding is the principle that:
- Each component exposes a **clean interface** (what it can do)
- It hides its **internal implementation** (how it does it)
- Other components don't need to know the internal details

**Simple analogy:** A TV remote exposes buttons (interface). You don't need to know how the infrared signal works internally.

---

### 7.2 How We Apply It in COS

#### Module: `menu_service.py`

| Exposed (Public) | Hidden (Internal) |
|-----------------|-------------------|
| `get_all_items()` | SQL query structure |
| `get_item_by_id(id)` | Database connection details |
| `update_item(id, data)` | How availability flag is stored |

> The Flask route just calls `menu_service.get_all_items()`. It doesn't know or care how the DB query works.

---

#### Module: `cart_service.py`

| Exposed (Public) | Hidden (Internal) |
|-----------------|-------------------|
| `add_to_cart(session_id, item_id, qty)` | How session data is structured |
| `remove_from_cart(session_id, item_id)` | localStorage sync logic |
| `get_cart(session_id)` | Total calculation formula |
| `clear_cart(session_id)` | Internal cart data structure |

---

#### Module: `payment_simulator.py`

| Exposed (Public) | Hidden (Internal) |
|-----------------|-------------------|
| `process_payment(amount, method)` → `{success: bool}` | How success/failure is decided |

> The checkout route only calls `process_payment()` and checks the result. It never needs to know what happens inside the simulator.

---

#### Module: `promo_service.py`

| Exposed (Public) | Hidden (Internal) |
|-----------------|-------------------|
| validate_code(code) → {valid, discount} | How promo expiry and discount are checked |
| `apply_code(cart, code)` | How discount is calculated |

---

#### Module: `order_service.py`

| Exposed (Public) | Hidden (Internal) |
|-----------------|-------------------|
| `create_order(cart, order_type, payment_method)` → `order_id` | ID generation algorithm |
| `get_order(order_id)` | DB schema / column names |
| `update_status(order_id, status)` | Internal status state machine |

---

### 7.3 Why This Matters for a 3-Person Team

| Benefit | Practical Meaning |
|---------|-------------------|
| **Parallel work** | Student A works on `menu_service`, Student B on `cart_service` — no conflicts |
| **Easy to test** | Each module can be tested independently without running the whole app |
| **Easy to fix bugs** | If cart total is wrong, you only look in `cart_service.py` |
| **Easy to swap parts** | If you want to change from JSON to SQLite, only the service layer changes |

---

### 7.4 Folder Structure (Recommended)

```
cos/
├── app.py                  ← Flask app, routes only (no business logic here)
├── services/
│   ├── menu_service.py     ← Menu CRUD logic
│   ├── cart_service.py     ← Cart add/remove/total logic
│   ├── promo_service.py ← Promo validation + discount logic
│   ├── order_service.py    ← Order creation + status
│   └── payment_simulator.py← Mock payment logic
├── models/
│   └── database.py         ← SQLite connection + table setup
├── static/
│   ├── css/style.css
│   └── js/cart.js
└── templates/
    ├── menu.html
    ├── cart.html
    ├── checkout.html
    ├── confirmation.html
    ├── order_status.html
    └── admin/
        └── menu.html
```

> **Rule:** `app.py` only handles routing and HTTP. All logic lives in `services/`. The database is only touched through `models/database.py`.

---

## Phase 2 Summary

| Section | Deliverable | Status |
|---------|-------------|--------|
| Gherkin Scenarios | Core scenarios for 8 functional requirements and 5 edge cases | ✅ |
| UML Explanation | Use Case, Class, Component | ✅ |
| Sequence Diagrams | Happy path, failure path, admin flow | ✅ |
| Activity Diagrams | Place order, manage menu, stock validation | ✅ |
| API Contracts | 8 endpoints with request/response examples | ✅ |
| QA Refinement Loop | 3 rounds: functional, edge case, NFR | ✅ |
| Information Hiding | 5 modules with public/hidden breakdown | ✅ |

---


