"""
tests/test_integration_order_flow.py

Integration tests for the full order flow.
Uses the real Flask app and a fresh in-memory database for every test.
"""

import uuid
import json
import pytest

from app import app
from models.database import init_db, seed_data


# ── Helper: unique session ID so tests never share cart state ──
def new_session():
    return str(uuid.uuid4())


# ── Set up the Flask test client and reset the database before every test ──
@pytest.fixture(autouse=True)
def setup():
    """
    Runs before every test:
      1. Rebuilds the database schema (init_db).
      2. Seeds it with menu items and promo codes (seed_data).
      3. Puts Flask in test mode so errors surface clearly.
    """
    app.config["TESTING"] = True
    init_db()
    seed_data()


@pytest.fixture
def client():
    """Returns a Flask test client for making fake HTTP requests."""
    with app.test_client() as client:
        yield client


# ────────────────────────────────────────────────────────────────
# 1. Full happy-path: add item → checkout → order created
# ────────────────────────────────────────────────────────────────
def test_checkout_creates_order(client):
    """
    Steps:
      1. Add item 1 to the cart via POST /api/cart/add
      2. Checkout via POST /api/checkout
      3. Assert the response is 200 and contains a valid order_code
    """
    session_id = new_session()

    # ── Step 1: Add an item to the cart ──
    add_response = client.post(
        "/api/cart/add",
        data=json.dumps({
            "session_id": session_id,
            "item_id":    1,
            "quantity":   2
        }),
        content_type="application/json"
    )
    assert add_response.status_code == 200, (
        f"Expected 200 when adding item, got {add_response.status_code}"
    )

    # ── Step 2: Checkout ──
    checkout_response = client.post(
        "/api/checkout",
        data=json.dumps({
            "session_id":     session_id,
            "order_type":     "Dine-In",
            "table_number":   "4",
            "payment_method": "Cash"
        }),
        content_type="application/json"
    )
    checkout_data = json.loads(checkout_response.data)

    # ── Step 3: Verify the order was created ──
    assert checkout_response.status_code == 201, (
        f"Expected 201 from checkout, got {checkout_response.status_code}. "
        f"Response: {checkout_data}"
    )
    assert "order_code" in checkout_data, (
        "Response should contain an order_code"
    )
    # order_code should follow the ORD-XXXXX pattern
    assert checkout_data["order_code"].startswith("ORD-"), (
        f"order_code should start with 'ORD-', got: {checkout_data['order_code']}"
    )
    assert checkout_data.get("status") == "Pending", (
        "New order status should be 'Pending'"
    )


# ────────────────────────────────────────────────────────────────
# 2. Failed payment — no order should be inserted
# ────────────────────────────────────────────────────────────────
def test_failed_payment_creates_no_order(client):
    """
    Steps:
      1. Add item 1 to the cart
      2. Checkout using "Mock Card Fail" to trigger payment failure
      3. Assert the API returns an error (not 200)
      4. Assert no order_code is returned
    """
    session_id = new_session()

    # ── Step 1: Add an item to the cart ──
    add_response = client.post(
        "/api/cart/add",
        data=json.dumps({
            "session_id": session_id,
            "item_id":    1,
            "quantity":   1
        }),
        content_type="application/json"
    )
    assert add_response.status_code == 200, (
        f"Expected 200 when adding item, got {add_response.status_code}"
    )

    # ── Step 2: Attempt checkout with a failing payment method ──
    checkout_response = client.post(
        "/api/checkout",
        data=json.dumps({
            "session_id":     session_id,
            "order_type":     "Takeaway",
            "pickup_time":    "14:00",
            "payment_method": "Mock Card Fail"
        }),
        content_type="application/json"
    )
    checkout_data = json.loads(checkout_response.data)

    # ── Step 3: Verify the API returned an error ──
    assert checkout_response.status_code != 200, (
        "A failed payment should not return HTTP 200"
    )
    assert "error" in checkout_data, (
        "Response should contain an 'error' key when payment fails"
    )

    # ── Step 4: Verify no order_code was returned ──
    assert "order_code" not in checkout_data, (
        "No order_code should be returned when payment fails"
    )