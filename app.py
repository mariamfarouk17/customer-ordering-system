from flask import Flask, jsonify, render_template, redirect, url_for, request

from models.database import init_db, seed_data
from services.menu_service import get_all_items
from services.cart_service import add_to_cart, remove_from_cart
from services.promo_service import apply_promo_code

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