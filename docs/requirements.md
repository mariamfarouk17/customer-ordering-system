# 🍽️ Customer Ordering System (COS)
## Phase 1 — Requirement Discovery & Traceability

> **Goal:** Design, build, and validate an automated Customer Ordering sub-system by prioritizing architectural integrity over mere code generation.

---

## 📋 Table of Contents

1. [Actor Classification](#1-actor-classification)
2. [Functional Requirements](#2-functional-requirements)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [Traceability Heatmap](#4-traceability-heatmap)
5. [Persona Discovery — Edge Cases](#5-persona-discovery--edge-cases)
6. [Phase 1 Summary](#6-phase-1-summary)

---

## 1. Actor Classification

Three actor tiers define every external entity that interacts with or is affected by the system.

### 🟢 Primary Actor — Initiating

| Actor | Description | Goals |
|-------|-------------|-------|
| **Customer** | Directly interacts with the ordering UI to browse, select, and pay for food items | Browse menu · Search menu items · Add/remove items · Adjust quantities · Apply promo code · Choose dine-in or takeaway · Confirm order · View order status |

### 🟣 Supporting Actors — Secondary

| Actor | Description | Goals |
|-------|-------------|-------|
| **Cashier / Staff** | Assists customers at the counter and creates orders on behalf of customers | Create or modify orders on behalf of customers · Mark items as unavailable  |
| **System Admin** | Manages menu content, pricing, promotions, user accounts, and system configuration | CRUD menu items & categories · Add, update, and manage menu items and categories.|

### ⚫ Offstage Actors

| Actor | Description | Interaction |
|-------|-------------|-------------|
| **Data Storage** | Stores menu items, cart data, promo codes, and orders. It is not directly used by the customer. | Backend reads menu data and saves confirmed orders. |
| **Payment Simulator** | A mock payment component used instead of a real payment gateway. | Returns payment success or failure for testing checkout. |

### Actor Classification Rationale

| Actor | Tier | Rationale |
|-------|------|-----------|
| Customer | Primary | Directly initiates the core use case (placing an order) without being prompted |
| Cashier / Staff | Supporting | Enables or assists the primary use case but does not own the ordering journey |
| System Admin | Supporting | Maintains system integrity so the primary use case can succeed; acts outside the order flow |
| Data Storage | Offstage | It supports the system by storing and retrieving menu and order data, but it does not directly initiate any user interaction. |
| Payment Simulator | Offstage | It simulates external payment behavior for validation without requiring real payment gateway integration. |

---

## 2. Functional Requirements

All requirements follow the format **`COS-FRxxx`** (functional) and **`COS-NFRxxx`** (non-functional).  
Each maps to at least one actor and one feature area — ensuring **zero orphaned requirements**.

| ID | Requirement | Description | Actors | Feature Area |
|----|-------------|-------------|--------|--------------|
| `COS-FR001` | **Browse & Search Menu** | The system shall display menu items grouped by category with names, prices, and availability status. | Customer, Admin | Browsing |
| `COS-FR002` | **Cart Management** | A customer shall add, remove, and update the quantity of items in a persistent shopping cart. Cart state shall survive page reload for at least 30 minutes. | Customer, Cashier | Cart |
| `COS-FR003` | **Order Type Selection** | The customer shall select **Dine-In** (with table number), **Takeaway** (with pick-up time) | Customer, Cashier | Order Fulfilment |
| `COS-FR004` | **Discount & Promo Code Application** | The system shall accept promotion codes, validate expiry and eligibility, and adjust the order total accordingly. Only one code per order unless configured otherwise. | Customer, Cashier, Admin | Pricing |
| `COS-FR005` | **Payment Processing** |The system shall simulate payment by allowing the customer to choose Cash or Mock Card payment and return success or failure.| Customer, Cashier, Payment Simulator | Checkout |
| `COS-FR006` | **Order Confirmation & Receipt** | On successful payment, the system shall generate a unique order ID, display an on-screen confirmation | Customer, Data Storage | Checkout |
| `COS-FR007` | **Live Order Status Tracking** | The customer shall view a simple order status page showing Pending, Confirmed, or Cancelled. | Customer, Data Storage | Real-time |
| `COS-FR008` | **Menu & Inventory Management** | System Admin shall add, update, and mark menu items as unavailable. | Admin | Menu Management |


---

## 3. Non-Functional Requirements

| ID | Requirement | Description | Actors | Feature Area |
|----|-------------|-------------|--------|--------------|
| `COS-NFR001` | **Performance** | Menu page initial load shall complete in ≤ 2 seconds on a 4G connection. Checkout submission shall return a response within 3 seconds under 200 concurrent users. | All actors | Performance |
| `COS-NFR002` | **Security** | The backend shall validate prices, item IDs, and quantities server-side and shall not trust client-submitted totals. | Customer, Payment GW | Compliance |
| `COS-NFR003` | **Availability** | The system shall handle invalid inputs without crashing and shall display clear error messages.| All actors | Reliability |
| `COS-NFR004` | **Accessibility** | The customer shall complete checkout in no more than 5 steps.| Customer | Compliance |

---

## 4. Traceability Heatmap

Every requirement is mapped to at least one actor and one feature area.

- **H** = High coverage (primary driver)
- **M** = Medium (participant / indirect)
- _(blank)_ = No direct relationship

| Req ID | Customer | Cashier | Admin | Data Storage | Payment Simulator | Feature Area |
|--------|:--------:|:-------:|:-----:|:------------:|:-----------------:|--------------|
| `COS-FR001` | H | | M | M | | Browsing |
| `COS-FR002` | H | M | | H | | Cart |
| `COS-FR003` | H | M | | | | Order Fulfilment |
| `COS-FR004` | H | M | M | | | Pricing |
| `COS-FR005` | H | M | | | H | Checkout |
| `COS-FR006` | H | | | H | M | Checkout |
| `COS-FR007` | H | | | H | | Order Status |
| `COS-FR008` | | | H | H | | Menu Management |
| `COS-NFR001` | H | M | | M | | Performance |
| `COS-NFR002` | H | M | M | H | | Security |
| `COS-NFR003` | H | H | M | M | M | Reliability |
| `COS-NFR004` | H | | M | | | Usability |

> ✅ Zero orphaned requirements — every requirement maps to at least one actor and one feature area.

---

## 5. Persona Discovery — Edge Cases

The **AI User Avatar** adopts two personas to uncover hidden requirements:

- 🤕 **The Frustrated Customer** — anxious, easily confused, poor/intermittent connectivity
- 😈 **The Malicious Actor** — attempts to exploit race conditions, API tampering, and brute-force attacks

---

### EC-01 — Double Payment on Network Timeout

> 🔴 **Severity: Critical**

**Persona (Frustrated Customer):**
> *"I hit Pay and got a spinner. After 10 seconds I clicked Pay again — my card was charged twice."*

**Root Cause:** No idempotency mechanism on the checkout endpoint; the server treated each POST as a new payment intent.

**Hidden Requirement `COS-FR013` — Idempotent Checkout:**
The checkout endpoint shall be idempotent. A unique idempotency key (cart ID + timestamp hash) shall be generated client-side and sent with every payment request. Duplicate submissions within 60 seconds using the same key shall return the original result without re-charging the customer.

**Tags:** `Payment Gateway` · `Idempotency` · `Checkout`

---

### EC-02 — Price Manipulation via API Tampering

> 🔴 **Severity: Critical**

**Persona (Malicious Actor):**
> *"I intercepted the POST /checkout request in Burp Suite and changed item prices to £0.01 before sending."*

**Root Cause:** The server trusted the client-submitted total without re-validating against the database.

**Hidden Requirement `COS-FR014` — Server-Side Price Validation:**
The server shall **never** trust client-submitted prices. The order total shall be computed server-side by fetching authoritative prices from the database at checkout time. Any mismatch between the client-submitted total and the server-computed total shall reject the order with HTTP `422 Unprocessable Entity` and log a security alert with session ID and IP address.

**Tags:** `Security` · `Checkout` · `Pricing`

---

### EC-03 — Cart Lost on Connectivity Drop

> 🟡 **Severity: High**

**Persona (Frustrated Customer):**
> *"I spent 5 minutes customising my order, my phone lost WiFi, and my whole cart vanished when the page reloaded."*

**Root Cause:** Cart state was stored only in memory; no server-side persistence or offline fallback existed.

**Hidden Requirement `COS-FR015` — Resilient Cart Persistence:**
Cart contents shall be persisted to a server-side session keyed to the customer's session token, and additionally cached in `localStorage` as a fallback. On page reload, the system shall restore cart state from the server session if available, or from `localStorage` if offline, displaying a banner to indicate the restored state.

**Tags:** `Customer` · `Cart` · `Resilience`

---

### EC-04 Invalid Promo Code Attempts

> 🟡 **Severity: High**

**Persona (Malicious Actor):**
> *"I wrote a script to try 10,000 promo codes in a loop — SAVE10, SAVE20, SAVE30 — until one worked."*

**Root Cause:** The promo-code validation endpoint had no rate limiting or attempt throttling.

**Hidden Requirement `COS-FR016` — Rate Limiting on Promo Code Endpoint:**
The promo-code validation endpoint shall apply rate limiting of ≤ 5 failed attempts per session per 10-minute window. On exceeding this threshold, the endpoint shall return HTTP `429 Too Many Requests` and lock that session from further code attempts for 15 minutes. Every breach shall be logged with session ID and IP address.

**Tags:** `Security` · `Rate Limiting` · `Pricing`

---

### EC-05 — Item Sold Out After Cart Addition

> 🔵 **Severity: Medium**

**Persona (Frustrated Customer):**
> *"I added the last portion of Chicken Shawarma to my cart, went to pay 10 minutes later, and the payment failed with 'item unavailable' — with no explanation of what to do next."*

**Root Cause:** Stock availability was only checked at the time of menu load, not at checkout submission.

**Hidden Requirement `COS-FR017` — Real-Time Stock Validation at Checkout:**
At checkout submission, the system shall perform a real-time stock validation for all cart items. If any item is unavailable, the response shall list the affected items clearly with an option to remove them and re-price the order. The customer shall **not** be charged. The cart shall remain intact to allow partial checkout without re-entry.

**Tags:** `Customer` · `Inventory` · `Cart` · `Checkout`

---

---

## 6. Phase 1 Summary

| Metric | Result |
|--------|--------|
| Actors classified | 5 (1 Primary · 2 Supporting · 2 Offstage) |
| Functional requirements | 8 (COS-FR001 – COS-FR008) |
| Non-functional requirements | 4 (COS-NFR001 – COS-NFR004) |
| Hidden requirements discovered | 5 (COS-FR013 – COS-FR017) |
| Orphaned requirements | **0** |
| Edge cases uncovered | **5** (requirement: ≥ 5 ✅) |
| AI Personas used | 2 (Frustrated Customer · Malicious Actor) |

---
