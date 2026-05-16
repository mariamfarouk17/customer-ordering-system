from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.order import Order, OrderItem