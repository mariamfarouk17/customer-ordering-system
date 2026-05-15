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

    # Check that the cart was really created in the database
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
        "session_id": "test_zero_quantity",
        "item_id": 1,
        "quantity": 0
    })

    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Quantity must be at least 1"