from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)

    # Relationship with OrderItem
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id}, Status: {self.status}>"

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)  # Assuming item_id corresponds to a menu item
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<OrderItem {self.id}, Order: {self.order_id}, Item: {self.item_id}, Quantity: {self.quantity}>"