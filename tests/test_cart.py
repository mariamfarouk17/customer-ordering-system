import pytest
from app import app
from database import create_tables, get_db_connection


def test_add_item_to_cart_api_updates_total():
    client = app.test_client()

    conn = get_db_connection(":memory:")
    create_tables(conn)

    conn.execute("""
        INSERT INTO menu_items (id, name, category, price, is_available)
        VALUES (1, 'Chicken Shawarma', 'Wraps', 100.0, 1)
    """)
    conn.commit()

    response = client.post("/api/cart/add", json={
        "session_id": "user123",
        "item_id": 1,
        "quantity": 2
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["cart_total"] == 200.0
    assert data["message"] == "Item added to cart"