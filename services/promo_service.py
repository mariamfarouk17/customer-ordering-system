from models.database import get_connection
from services.cart_service import calculate_cart_total


def apply_promo_code(session_id, code):
    if session_id is None:
        return {"error": "Session ID is required"}

    if code is None or code.strip() == "":
        return {"error": "Promo code is required"}

    code = code.strip().upper()

    with get_connection() as conn:
        cart = conn.execute(
            "SELECT id FROM carts WHERE session_id = ?",
            (session_id,)
        ).fetchone()

        if cart is None:
            return {"error": "Cart not found"}

        cart_id = cart["id"]
        cart_total = calculate_cart_total(conn, cart_id)

        promo = conn.execute("""
            SELECT code, discount_percent, is_active
            FROM promo_codes
            WHERE code = ?
        """, (code,)).fetchone()

        if promo is None or promo["is_active"] == 0:
            return {
                "error": "Invalid promo code",
                "cart_total": cart_total
            }

        discount_amount = cart_total * (promo["discount_percent"] / 100)
        new_total = cart_total - discount_amount

        return {
            "message": "Promo code applied",
            "discount_percent": promo["discount_percent"],
            "discount_amount": discount_amount,
            "new_total": new_total
        }