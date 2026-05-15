from flask import Flask, request, jsonify
from cart_service import add_to_cart

app = Flask(__name__)

@app.route("/api/cart/add", methods=["POST"])
def cart_add():
    data = request.get_json()
    session_id = data["session_id"]
    item_id = data["item_id"]
    quantity = data["quantity"]
    result = add_to_cart(session_id, item_id, quantity)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)