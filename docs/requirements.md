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
| **Customer** | Directly interacts with the ordering UI to browse, select, customise, and pay for food items | Browse menu by category / search · Add/remove items, adjust quantities · Apply discount codes & loyalty points · Choose dine-in, takeaway, or delivery · Pay and receive order confirmation · Track live order status |

### 🟣 Supporting Actors — Secondary

| Actor | Description | Goals |
|-------|-------------|-------|
| **Cashier / Staff** | Assists customers at the counter, handles special requests, and overrides the system when needed | Create or modify orders on behalf of customers · Apply manual discounts or voids · Mark items as unavailable · Process cash payments |
| **System Admin** | Manages menu content, pricing, promotions, user accounts, and system configuration | CRUD menu items & categories · Configure tax rates & fees · Manage staff accounts & roles · Configure integration endpoints |

### ⚫ Offstage Actors

| Actor | Description | Interaction |
|-------|-------------|-------------|
| **Payment Gateway** | Processes card/digital-wallet transactions. Never directly visible to the customer UI layer | Authorise & capture charges · Return success / failure / 3DS challenge · Issue refunds on request |
| **Notification Service** | Sends SMS/email order confirmations and status updates. Acts on system events, not direct requests | Order confirmation on payment success · Ready/dispatched status alerts · Failed-payment retry prompts |
| **Kitchen Display System (KDS)** | Receives confirmed orders as a downstream consumer. Does not initiate any ordering flows | Receive new order tickets · Acknowledge item completion · Signal order-ready back to COS |

### Actor Classification Rationale

| Actor | Tier | Rationale |
|-------|------|-----------|
| Customer | Primary | Directly initiates the core use case (placing an order) without being prompted |
| Cashier / Staff | Supporting | Enables or assists the primary use case but does not own the ordering journey |
| System Admin | Supporting | Maintains system integrity so the primary use case can succeed; acts outside the order flow |
| Payment Gateway | Offstage | Fulfils a required function but has no UI presence; interaction is API-only |
| Notification Service | Offstage | Reacts to system events; invisible to customer during ordering |
| Kitchen Display System | Offstage | Downstream consumer; cannot initiate or cancel orders |

---

## 2. Functional Requirements

All requirements follow the format **`COS-FRxxx`** (functional) and **`COS-NFRxxx`** (non-functional).  
Each maps to at least one actor and one feature area — ensuring **zero orphaned requirements**.

| ID | Requirement | Description | Actors | Feature Area |
|----|-------------|-------------|--------|--------------|
| `COS-FR001` | **Browse & Search Menu** | The system shall display menu items grouped by category with images, descriptions, prices, and allergen flags. A real-time search with fuzzy matching shall be available. | Customer, Admin | Browsing |
| `COS-FR002` | **Cart Management** | A customer shall add, remove, and update the quantity of items in a persistent shopping cart. Cart state shall survive page reload for at least 30 minutes. | Customer, Cashier | Cart |
| `COS-FR003` | **Item Customisation** | The system shall allow selection of modifiers (size, extras, removals, cooking preference) with prices adjusted dynamically. Invalid combinations shall be blocked. | Customer, Cashier, Admin | Cart |
| `COS-FR004` | **Order Type Selection** | The customer shall select **Dine-In** (with table number), **Takeaway** (with pick-up time), or **Delivery** (with address & delivery fee) before checkout. | Customer, Cashier | Order Fulfilment |
| `COS-FR005` | **Discount & Promo Code Application** | The system shall accept promotion codes, validate expiry and eligibility, and adjust the order total accordingly. Only one code per order unless configured otherwise. | Customer, Cashier, Admin | Pricing |
| `COS-FR006` | **Payment Processing** | The system shall integrate with the Payment Gateway to process card, digital wallet, and cash payments. Payment status (success, failure, pending) shall be reflected to the customer within 5 seconds. | Customer, Cashier, Payment GW | Checkout |
| `COS-FR007` | **Order Confirmation & Receipt** | On successful payment, the system shall generate a unique order ID, display an on-screen confirmation, and trigger the Notification Service to dispatch an SMS/email receipt. | Customer, Notification Service | Checkout |
| `COS-FR008` | **Order Transmission to KDS** | After payment confirmation, the system shall publish the order (items, modifiers, priority, order type) to the Kitchen Display System within **2 seconds** via a reliable message queue. | KDS | Order Fulfilment |
| `COS-FR009` | **Live Order Status Tracking** | The customer shall view a live status page (Received → Preparing → Ready → Collected). Status updates shall be pushed via **WebSocket** with no manual refresh required. | Customer, KDS | Real-time |
| `COS-FR010` | **Staff Order Override** | Cashier accounts shall be able to create, modify, or cancel any order on behalf of a customer with a mandatory reason code logged for every modification. | Cashier, Admin | Audit |
| `COS-FR011` | **Menu & Inventory Management** | System Admin shall create, update, deactivate, and delete menu items, categories, and modifier groups. Changes shall propagate to the customer-facing menu within **30 seconds**. | Admin | Menu Management |
| `COS-FR012` | **Refund Processing** | Authorised staff shall initiate full or partial refunds for completed orders. The system shall call the Payment Gateway refund endpoint and log the transaction with the initiating staff ID. | Cashier, Payment GW | Audit |

---

## 3. Non-Functional Requirements

| ID | Requirement | Description | Actors | Feature Area |
|----|-------------|-------------|--------|--------------|
| `COS-NFR001` | **Performance** | Menu page initial load shall complete in ≤ 2 seconds on a 4G connection. Checkout submission shall return a response within 3 seconds under 200 concurrent users. | All actors | Performance |
| `COS-NFR002` | **Security & PCI-DSS** | No raw card data shall be stored or logged by the COS. All payment data shall be tokenised by the Payment Gateway. All communication shall use TLS 1.2+. | Customer, Payment GW | Compliance |
| `COS-NFR003` | **Availability** | The system shall achieve 99.5% uptime during operating hours. Degraded mode shall allow order browsing even if the payment gateway is temporarily unavailable. | All actors | Reliability |
| `COS-NFR004` | **Accessibility** | The customer-facing UI shall conform to WCAG 2.1 AA. All interactive elements shall be keyboard-navigable and screen-reader compatible. | Customer | Compliance |

---

## 4. Traceability Heatmap

Every requirement is mapped to at least one actor and one feature area.

- **H** = High coverage (primary driver)
- **M** = Medium (participant / indirect)
- _(blank)_ = No direct relationship

| Req ID | Customer | Cashier | Admin | Pay. GW | Notif. | KDS | Feature Area |
|--------|:--------:|:-------:|:-----:|:-------:|:------:|:---:|--------------|
| `COS-FR001` | H | | M | | | | Browsing |
| `COS-FR002` | H | M | | | | | Cart |
| `COS-FR003` | H | M | M | | | | Cart |
| `COS-FR004` | H | M | | | | M | Order Fulfilment |
| `COS-FR005` | H | H | M | | | | Pricing |
| `COS-FR006` | H | M | | H | | | Checkout |
| `COS-FR007` | H | | | M | H | | Checkout |
| `COS-FR008` | | | | | | H | Order Fulfilment |
| `COS-FR009` | H | | | | | M | Real-time |
| `COS-FR010` | M | H | M | M | | | Audit |
| `COS-FR011` | M | | H | | | M | Menu Management |
| `COS-FR012` | M | H | | H | M | | Audit |
| `COS-NFR001` | H | M | | M | | M | Performance |
| `COS-NFR002` | H | M | M | H | | | Security |
| `COS-NFR003` | H | H | M | M | M | M | Reliability |
| `COS-NFR004` | H | | M | | | | Accessibility |

> ✅ **Zero orphaned requirements** — every actor appears in ≥ 1 requirement. Every requirement traces to ≥ 1 actor and ≥ 1 feature area.

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

### EC-04 — Promo Code Brute-Force Enumeration

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

### EC-06 — Order Confirmed but KDS Never Receives It

> 🔵 **Severity: Medium**

**Persona (Frustrated Customer):**
> *"Payment went through fine but the kitchen never got my order. Staff had no idea what I'd ordered."*

**Root Cause:** KDS transmission was fire-and-forget with no delivery guarantee or alerting mechanism.

**Hidden Requirement `COS-FR018` — Guaranteed KDS Delivery with Fallback:**
The system shall use a **persistent message queue** (at-least-once delivery) for KDS transmission. If a KDS acknowledgement is not received within 10 seconds, the system shall retry up to 3 times with exponential back-off, then alert on-duty staff via the management dashboard with the full order details for manual entry. All retry attempts shall be logged.

**Tags:** `KDS` · `Order Fulfilment` · `Reliability`

---

## 6. Phase 1 Summary

| Metric | Result |
|--------|--------|
| Actors classified | 6 (1 Primary · 2 Supporting · 3 Offstage) |
| Functional requirements | 12 (COS-FR001 – COS-FR012) |
| Non-functional requirements | 4 (COS-NFR001 – COS-NFR004) |
| Hidden requirements discovered | 6 (COS-FR013 – COS-FR018) |
| Orphaned requirements | **0** |
| Edge cases uncovered | **6** (requirement: ≥ 5 ✅) |
| AI Personas used | 2 (Frustrated Customer · Malicious Actor) |

---
