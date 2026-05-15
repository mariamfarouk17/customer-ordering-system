from app import app
from models.database import init_db, seed_data


def test_add_available_item_to_cart_updates_total():
    init_db()
    seed_data()

    client = app.test_client()

    response = client.post("/api/cart/add", json={
        "session_id": "test_user_123",
        "item_id": 1,
        "quantity": 2
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Item added to cart"
    assert data["cart_total"] == 13.0