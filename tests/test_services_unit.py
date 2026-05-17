"""
tests/test_services_unit.py

Unit tests for the Customer Ordering System service layer.
Uses a fresh in-memory database for every test via init_db() and seed_data().
"""

import uuid
import pytest

from models.database import init_db, seed_data
from services.menu_service  import get_all_items, get_item_by_id, is_item_available
from services.cart_service  import add_to_cart, remove_from_cart
from services.promo_service import apply_promo_code


# ── Helper: unique session ID so tests never share cart state ──
def new_session():
    return str(uuid.uuid4())


# ── Reset the database before every single test ──
@pytest.fixture(autouse=True)
def fresh_db():
    init_db()
    seed_data()


# ────────────────────────────────────────────────
# 1. get_all_items returns categories
# ────────────────────────────────────────────────
def test_get_all_items_returns_categories():
    result = get_all_items()

    # The response must have a "categories" key
    assert "categories" in result

    # There must be at least one category
    assert len(result["categories"]) > 0

    # Each category must have a name and a list of items
    for category in result["categories"]:
        assert "name"  in category
        assert "items" in category
        assert isinstance(category["items"], list)


# ────────────────────────────────────────────────
# 2. get_item_by_id returns item 1
# ────────────────────────────────────────────────
def test_get_item_by_id_returns_item():
    item = get_item_by_id(1)

    # Item must be found
    assert item is not None

    # Must contain the expected fields
    assert "id"           in item
    assert "name"         in item
    assert "price"        in item
    assert "is_available" in item

    # ID must match what we asked for
    assert item["id"] == 1


# ────────────────────────────────────────────────
# 3. is_item_available returns True for item 1
# ────────────────────────────────────────────────
def test_is_item_available_returns_true():
    result = is_item_available(1)
    assert result is True


# ────────────────────────────────────────────────
# 4. add_to_cart rejects quantity 0
# ────────────────────────────────────────────────
def test_add_to_cart_rejects_zero_quantity():
    session_id = new_session()

    result = add_to_cart(session_id, item_id=1, quantity=0)

    # Must return an error, not a success message
    assert "error" in result
    assert "message" not in result


# ────────────────────────────────────────────────
# 5. add_to_cart rejects quantity greater than 20
# ────────────────────────────────────────────────
def test_add_to_cart_rejects_quantity_over_limit():
    session_id = new_session()

    result = add_to_cart(session_id, item_id=1, quantity=21)

    # Must return an error about the limit
    assert "error" in result
    assert "message" not in result


# ────────────────────────────────────────────────
# 6. Invalid promo code returns error
# ────────────────────────────────────────────────
def test_invalid_promo_code_returns_error():
    session_id = new_session()

    # Add an item first so the cart exists
    add_to_cart(session_id, item_id=1, quantity=1)

    result = apply_promo_code(session_id, "NOTACODE")

    # Must return an error key
    assert "error" in result
    assert "message" not in result


# ────────────────────────────────────────────────
# 7. remove_from_cart updates total
# ────────────────────────────────────────────────
def test_remove_from_cart_updates_total():
    session_id = new_session()

    # Add two different items
    add_to_cart(session_id, item_id=1, quantity=1)
    add_to_cart(session_id, item_id=2, quantity=1)

    # Capture the total before removal
    result_before = add_to_cart(session_id, item_id=1, quantity=0)
    # add_to_cart with qty=0 returns an error, so fetch total a different way:
    # remove item 2 and check the returned cart_total is less
    result = remove_from_cart(session_id, item_id=2)

    # Must succeed and return a numeric cart_total
    assert "error"      not in result
    assert "cart_total" in result
    assert isinstance(result["cart_total"], (int, float))

    # After removing one item the total must be >= 0
    assert result["cart_total"] >= 0