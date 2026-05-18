# customer-ordering-system
Software Engineering term project for designing and validating a Customer Ordering System using Python backend architecture.
# Customer Ordering System

Software Engineering term project for CSE323.

## Team Members
- Mariam 034
- Mairoum 136
- Maram 175

## Sub-system
Customer Ordering System

## Tech Stack
- Backend: Python (Flask/FastAPI)
- Frontend: HTML/CSS/JS
- Testing: Pytest + Playwright

## Features
- Browse menu
- Add items to cart
- Checkout orders
- Order validation
- Order tracking
# Customer Ordering System (COS)

A Flask-based Customer Ordering System that allows customers to browse menu items, search items, add items to a cart, apply promo codes, complete checkout, and receive an order confirmation.

This project was developed as part of a Software Engineering course using requirements analysis, design specification, test-driven implementation, and validation evidence.

---

## Project Overview

The Customer Ordering System focuses on automating the ordering process for a restaurant or café.  
The system supports the customer journey from viewing the menu to placing an order.

The main goal of the project is not only to generate code, but to demonstrate a complete software engineering process:

- Requirements discovery
- Actor classification
- Traceability mapping
- Gherkin scenarios
- UML and system design
- API contracts
- Test-Driven Prompting evidence
- Validation and testing pyramid evidence

---

## Implemented Features

### 1. Menu Browsing and Search

Customers can view menu items grouped by category.

Each item displays:

- Item name
- Price
- Availability status
- Food image

Customers can also search for menu items by name.

---

### 2. Cart Management

Customers can:

- Add available items to the cart
- Select item quantity
- Remove items from the cart
- View updated cart total
- Clear the cart

The cart total is calculated by the backend using server-side prices.

---

### 3. Promo Code Application

Customers can apply a promo code from the menu page.

Supported behavior:

- Valid promo codes apply a discount
- Invalid promo codes show an error message
- Invalid promo codes do not change the cart total

Example promo code:

```text
SAVE10
```

---

### 4. Checkout and Order Confirmation

Customers can proceed to checkout, choose an order type and payment method, then submit the order.

The system creates an order and displays a confirmation page with an order code.

---

### 5. Backend API

The system exposes Flask API routes for menu, cart, promo, checkout, and order retrieval.

---

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Pytest
- Playwright
- Git and GitHub

---

## Project Structure

```text
customer-ordering-system/
├── app.py
├── models/
│   ├── __init__.py
│   └── database.py
├── services/
│   ├── __init__.py
│   ├── menu_service.py
│   ├── cart_service.py
│   ├── promo_service.py
│   ├── order_service.py
│   └── payment_simulator.py
├── templates/
│   ├── menu.html
│   ├── checkout.html
│   └── confirmation.html
├── static/
│   └── images/
├── tests/
│   ├── test_menu.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   ├── test_services_unit.py
│   └── test_integration_order_flow.py
├── e2e/
│   ├── pages/
│   │   └── menu_page.py
│   └── test_customer_order_flow.py
├── docs/
└── README.md
```

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-link>
cd customer-ordering-system
```

### 2. Create a virtual environment

On Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the main packages manually:

```bash
pip install flask pytest pytest-playwright playwright
python -m playwright install
```

### 4. Run the Flask application

```bash
py app.py
```

or:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000/menu
```

---

## Testing

The project includes automated tests for menu, cart, promo, checkout, and order flow.

### Run all tests

```bash
py -m pytest
```

or:

```bash
python -m pytest
```

---

## Testing Pyramid

The validation phase follows the testing pyramid concept:

| Layer | Description |
|---|---|
| Unit Tests | Service-level and validation tests |
| Integration Tests | Full API order flow tests |
| E2E Tests | Playwright customer ordering flow |

The project includes:

- Unit tests for service behavior
- Integration tests for order flow
- Playwright E2E test for the customer journey

---

## Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/menu` | Returns menu items grouped by category |
| POST | `/api/cart/add` | Adds an item to the cart |
| POST | `/api/cart/remove` | Removes an item from the cart |
| POST | `/api/promo/apply` | Applies a promo code |
| POST | `/api/checkout` | Processes checkout and creates an order |
| GET | `/api/order/<order_code>` | Retrieves order details |

---

## Software Engineering Deliverables

### D2 — Requirements Report

Includes:

- Actor classification
- Functional requirements
- Non-functional requirements
- Traceability heatmap
- Persona-based edge cases

### D3 — Design Specification

Includes:

- Gherkin scenarios
- UML diagrams
- System Sequence Diagrams
- Activity diagrams
- API contracts
- QA refinement loop
- Information hiding

### D4 — Validation Report

Includes:

- Testing pyramid results
- Unit test evidence
- Integration test evidence
- Playwright E2E evidence
- Verification vs Validation statement

### D5 — Implementation Package

Includes:

- Source code
- GitHub repository
- Test-Driven Prompting evidence
- Vertical slice implementation evidence

---

## Development Approach

This project was developed using vertical slicing and Test-Driven Prompting.

Each slice connects multiple layers of the system:

```text
UI → API Route → Service Logic → Database → Test
```

Implemented vertical slices include:

- Menu slice
- Cart and promo slice
- Checkout and order slice

---

## Validation Summary

### Verification

Verification answers the question:

```text
Did we build the system correctly?
```

The tests verify that menu loading, cart operations, promo code handling, checkout, and order creation work correctly.

### Validation

Validation answers the question:

```text
Did we build the right system?
```

The system solves the customer ordering problem by allowing customers to browse items, manage a cart, apply discounts, checkout, and receive confirmation.

---

## Team Responsibilities

| Student | Main Responsibility |
|---|---|
| mariam034 | Menu browsing and search |
| mairoun136| Cart and promo code |
| maram175 | Checkout, order, and validation flow |

---

## Notes

- SQLite database files and cache folders are ignored from Git.
- The backend recalculates prices server-side instead of trusting frontend totals.
- Playwright tests require the Flask server to be running before execution.
- Some admin and tracking features are documented in the design specification as project scope and future extension areas.

---

## Repository Purpose

This repository demonstrates a complete software engineering workflow for a Customer Ordering System, including analysis, design, implementation, testing, and validation.

```
