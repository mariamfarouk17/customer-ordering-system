import uuid

from app import app
from models.database import init_db, seed_data, get_connection


def test_add_available_item_to_cart_updates_total():
    init_db()
    seed_data()

    client = app.test_client()

    session_id = "test_user_" + str(uuid.uuid4())

    response = client.post("/api/cart/add", json={
        "session_id": session_id,
        "item_id": 1,
        "quantity": 2
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Item added to cart"
    assert data["cart_total"] == 13.0

    with get_connection() as conn:
        cart = conn.execute(
            "SELECT id, session_id FROM carts WHERE session_id = ?",
            (session_id,)
        ).fetchone()

        assert cart is not None

        cart_item = conn.execute(
            "SELECT menu_item_id, quantity FROM cart_items WHERE cart_id = ?",
            (cart["id"],)
        ).fetchone()

        assert cart_item is not None
        assert cart_item["menu_item_id"] == 1
        assert cart_item["quantity"] == 2


def test_add_item_rejects_zero_quantity():
    init_db()
    seed_data()

    client = app.test_client()

    response = client.post("/api/cart/add", json={
        "session_id": "test_zero_quantity_" + str(uuid.uuid4()),
        "item_id": 1,
        "quantity": 0
    })

    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Quantity must be at least 1"


def test_add_item_rejects_negative_quantity():
    init_db()
    seed_data()

    client = app.test_client()

    response = client.post("/api/cart/add", json={
        "session_id": "test_negative_quantity_" + str(uuid.uuid4()),
        "item_id": 1,
        "quantity": -1
    })

    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Quantity must be at least 1"


def test_remove_item_from_cart_updates_total():
    init_db()
    seed_data()

    client = app.test_client()

    session_id = "test_remove_" + str(uuid.uuid4())

    add_response = client.post("/api/cart/add", json={
        "session_id": session_id,
        "item_id": 1,
        "quantity": 2
    })

    assert add_response.status_code == 200

    remove_response = client.post("/api/cart/remove", json={
        "session_id": session_id,
        "item_id": 1
    })

    data = remove_response.get_json()

    assert remove_response.status_code == 200
    assert data["message"] == "Item removed from cart"
    assert data["cart_total"] == 0


def test_invalid_promo_code_does_not_change_total():
    init_db()
    seed_data()

    client = app.test_client()

    session_id = "test_invalid_promo_" + str(uuid.uuid4())

    add_response = client.post("/api/cart/add", json={
        "session_id": session_id,
        "item_id": 1,
        "quantity": 2
    })

    assert add_response.status_code == 200

    promo_response = client.post("/api/promo/apply", json={
        "session_id": session_id,
        "code": "FAKECODE"
    })

    data = promo_response.get_json()

    assert promo_response.status_code == 400
    assert data["error"] == "Invalid promo code"
    assert data["cart_total"] == 13.0


def test_valid_promo_code_applies_discount():
    init_db()
    seed_data()

    client = app.test_client()

    session_id = "test_valid_promo_" + str(uuid.uuid4())

    add_response = client.post("/api/cart/add", json={
        "session_id": session_id,
        "item_id": 1,
        "quantity": 2
    })

    assert add_response.status_code == 200

    promo_response = client.post("/api/promo/apply", json={
        "session_id": session_id,
        "code": "SAVE10"
    })

    data = promo_response.get_json()

    assert promo_response.status_code == 200
    assert data["message"] == "Promo code applied"
    assert data["discount_percent"] == 10.0
    assert data["discount_amount"] == 1.3
    assert data["new_total"] == 11.7
