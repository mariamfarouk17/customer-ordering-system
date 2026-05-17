from flask import Flask, jsonify, render_template, redirect, url_for, request

from models.database import init_db, seed_data
from services.menu_service import get_all_items
from services.cart_service import add_to_cart, remove_from_cart, calculate_cart_total
from services.promo_service import apply_promo_code
from services.order_service import create_order, get_order_by_code
from models.database import get_connection


app = Flask(__name__)


# -----------------------------
# Page Routes
# -----------------------------

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
    return render_template(
        "confirmation.html",
        order_code=order_code
    )


# -----------------------------
# API Routes
# -----------------------------
    


# --- API Routes ---

@app.route("/api/menu")
def api_menu():
    data = get_all_items()
    return jsonify(data), 200


@app.route("/api/cart/add", methods=["POST"])
def api_cart_add():
    data = request.get_json() or {}

    session_id = data.get("session_id")
    item_id = data.get("item_id")
    quantity = data.get("quantity")

    result = add_to_cart(session_id, item_id, quantity)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/api/cart/remove", methods=["POST"])
def api_cart_remove():
    data = request.get_json() or {}

    session_id = data.get("session_id")
    item_id = data.get("item_id")

    result = remove_from_cart(session_id, item_id)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/api/promo/apply", methods=["POST"])
def api_promo_apply():
    data = request.get_json() or {}

    session_id = data.get("session_id")
    code = data.get("code")

    result = apply_promo_code(session_id, code)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/api/checkout", methods=["POST"])
def api_checkout():
    data = request.get_json() or {}

    result = create_order(
        session_id=data.get("session_id"),
        order_type=data.get("order_type"),
        payment_method=data.get("payment_method"),
        table_number=data.get("table_number"),
        pickup_time=data.get("pickup_time")
    )

    if "error" in result:
        status_code = result.get("status_code", 400)

        # Remove status_code before sending response
        result.pop("status_code", None)

        return jsonify(result), status_code

    return jsonify(result), 201


@app.route("/api/order/<order_code>", methods=["GET"])
def api_get_order(order_code):
    result = get_order_by_code(order_code)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200
    


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
    return jsonify({"status": "ok"}), 200


# -----------------------------
# App Start
# -----------------------------

if __name__ == "__main__":
    init_db()
    seed_data()

    print("Starting Customer Ordering System...")
    app.run(debug=True, port=5002)
