from flask import Flask, jsonify, render_template, redirect, url_for, request

from models.database import init_db, seed_data
from services.menu_service import get_all_items
from services.cart_service import add_to_cart, remove_from_cart, calculate_cart_total, get_or_create_cart
from services.promo_service import apply_promo_code
from models.database import get_connection
import datetime
import random

app = Flask(__name__)


# --- Page Routes ---

@app.route("/")
def index():
    return redirect(url_for("menu"))


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/checkout")
def checkout_page():
    return render_template("checkout.html")


@app.route("/confirmation/<order_code>")
def confirmation_page(order_code):
    return render_template("confirmation.html", order_code=order_code)


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


@app.route("/api/checkout", methods=["POST"])
def api_checkout():
    data = request.get_json() or {}

    session_id = data.get("session_id")
    order_type = data.get("order_type")  # 'Dine-In' or 'Takeaway'
    payment_method = data.get("payment_method", "Cash")
    promo_code = data.get("promo_code")

    if not session_id:
        return jsonify({"error": "Session ID is required"}), 400

    with get_connection() as conn:
        cart = conn.execute("SELECT id FROM carts WHERE session_id = ?", (session_id,)).fetchone()
        if cart is None:
            return jsonify({"error": "Cart not found"}), 400

        cart_id = cart["id"]

        # Load cart items and validate availability
        rows = conn.execute(
            "SELECT ci.menu_item_id, ci.quantity, mi.price, mi.is_available, mi.name FROM cart_items ci JOIN menu_items mi ON ci.menu_item_id = mi.id WHERE ci.cart_id = ?",
            (cart_id,)
        ).fetchall()

        if not rows:
            return jsonify({"error": "Your cart is empty. Please add items before checkout."}), 400

        unavailable = [r["name"] for r in rows if r["is_available"] == 0]
        if unavailable:
            return jsonify({"error": "Some items are unavailable", "items": unavailable}), 422

        subtotal = calculate_cart_total(conn, cart_id)

        discount_amount = 0
        if promo_code:
            promo = conn.execute("SELECT discount_percent, is_active FROM promo_codes WHERE code = ?", (promo_code.strip().upper(),)).fetchone()
            if promo is None or promo["is_active"] == 0:
                return jsonify({"error": "Invalid promo code", "cart_total": subtotal}), 400
            discount_amount = subtotal * (promo["discount_percent"] / 100)

        total = max(0, subtotal - discount_amount)

        # Simulate payment (always succeed for this demo)
        payment_success = True

        if not payment_success:
            return jsonify({"error": "Payment failed"}), 402

        # Create order
        order_code = "ORD" + datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        created_at = datetime.datetime.utcnow().isoformat()

        cursor = conn.execute(
            "INSERT INTO orders (order_code, order_type, table_number, pickup_time, payment_method, status, subtotal, promo_code, discount_amount, total, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_code, order_type or "Takeaway", None, None, payment_method, "Confirmed", subtotal, promo_code, discount_amount, total, created_at)
        )

        order_id = cursor.lastrowid

        # Insert order items
        for r in rows:
            conn.execute(
                "INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, r["menu_item_id"], r["quantity"], r["price"])
            )

        # Clear cart items
        conn.execute("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))

        return jsonify({"message": "Order placed", "order_code": order_code, "total": total}), 200


@app.route("/api/order/<order_code>")
def api_get_order(order_code):
    with get_connection() as conn:
        order = conn.execute(
            "SELECT * FROM orders WHERE order_code = ?",
            (order_code,)
        ).fetchone()

        if order is None:
            return jsonify({"error": "Order not found"}), 404

        items = conn.execute(
            "SELECT oi.quantity, oi.unit_price, mi.name FROM order_items oi JOIN menu_items mi ON oi.menu_item_id = mi.id WHERE oi.order_id = ?",
            (order["id"],)
        ).fetchall()

        item_list = [
            {"name": i["name"], "quantity": i["quantity"], "unit_price": i["unit_price"]}
            for i in items
        ]

        return jsonify({
            "order_code": order["order_code"],
            "status": order["status"],
            "order_type": order["order_type"],
            "payment_method": order["payment_method"],
            "created_at": order["created_at"],
            "subtotal": order["subtotal"],
            "discount_amount": order["discount_amount"],
            "total": order["total"],
            "items": item_list
        }), 200


@app.route("/api/cart")
def api_get_cart():
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    with get_connection() as conn:
        cart = conn.execute("SELECT id FROM carts WHERE session_id = ?", (session_id,)).fetchone()
        if cart is None:
            return jsonify({"items": [], "subtotal": 0.0}), 200

        cart_id = cart["id"]

        rows = conn.execute(
            "SELECT ci.menu_item_id, ci.quantity, mi.price, mi.name FROM cart_items ci JOIN menu_items mi ON ci.menu_item_id = mi.id WHERE ci.cart_id = ?",
            (cart_id,)
        ).fetchall()

        items = [
            {"id": r["menu_item_id"], "name": r["name"], "quantity": r["quantity"], "unit_price": r["price"]}
            for r in rows
        ]

        subtotal = calculate_cart_total(conn, cart_id)

        return jsonify({"items": items, "subtotal": subtotal}), 200


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    init_db()
    seed_data()
    print("Starting Customer Ordering System...")
    app.run(debug=False, port=5002)
