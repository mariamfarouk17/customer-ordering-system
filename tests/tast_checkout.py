# File: test_checkout.py
import pytest
from app import app, db
from models import Order, OrderItem

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_checkout_creates_order(client):
    # Simulate cart data
    cart_data = {
        "items": [
            {"id": 1, "quantity": 2},
            {"id": 2, "quantity": 1}
        ],
        "payment_info": {"card_number": "4111111111111111", "expiry": "12/25"}
    }
    response = client.post('/api/checkout', json=cart_data)
    assert response.status_code == 201
    with app.app_context():
        orders = Order.query.all()
        assert len(orders) == 1  # Ensure an order is created

def test_payment_failure_creates_no_order(client):
    # Simulate cart data with invalid payment
    cart_data = {
        "items": [
            {"id": 1, "quantity": 2},
            {"id": 2, "quantity": 1}
        ],
        "payment_info": {"card_number": "0000000000000000", "expiry": "12/25"}
    }
    response = client.post('/api/checkout', json=cart_data)
    assert response.status_code == 400
    with app.app_context():
        orders = Order.query.all()
        assert len(orders) == 0  # Ensure no order is created