from flask import Flask, jsonify, render_template, redirect, url_for, request

from models.database import init_db, seed_data
from services.menu_service import get_all_items
from services.cart_service import add_to_cart, remove_from_cart
from services.promo_service import apply_promo_code
from flask import Flask, request, jsonify
from models import db, Order, OrderItem
from models.order import db
from models.order import Order, OrderItem

app = Flask(__name__)


# --- Page Routes ---

@app.route("/")
def index():
    return redirect(url_for("menu"))


@app.route("/menu")
def menu():
    return render_template("menu.html")


# --- API Routes ---

@app.route("/api/menu")
def api_menu():
    data = get_all_items()
    return jsonify(data)


@app.route("/api/cart/add", methods=["POST"])
def api_cart_add():
    data = request.get_json()

    session_id = data.get("session_id")
    item_id = data.get("item_id")
    quantity = data.get("quantity")

    result = add_to_cart(session_id, item_id, quantity)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/api/cart/remove", methods=["POST"])
def api_cart_remove():
    data = request.get_json()

    session_id = data.get("session_id")
    item_id = data.get("item_id")

    result = remove_from_cart(session_id, item_id)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/api/promo/apply", methods=["POST"])
def api_promo_apply():
    data = request.get_json()

    session_id = data.get("session_id")
    code = data.get("code")

    result = apply_promo_code(session_id, code)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    init_db()
    seed_data()
    print("Starting Customer Ordering System...")
    app.run(debug=True)

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json()

    # Validate cart data
    if not data or 'items' not in data or 'payment_info' not in data:
        return jsonify({"error": "Invalid request"}), 400

    items = data['items']
    payment_info = data['payment_info']

    # Simulate payment processing
    if payment_info['card_number'] == "0000000000000000":
        return jsonify({"error": "Payment failed"}), 400

    # Create order
    order = Order()
    db.session.add(order)
    db.session.flush()  # Get the order ID before committing

    for item in items:
        order_item = OrderItem(order_id=order.id, item_id=item['id'], quantity=item['quantity'])
        db.session.add(order_item)

    db.session.commit()

    return jsonify({"message": "Order created", "order_id": order.id}), 201   