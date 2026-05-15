from models.database import get_connection


def calculate_cart_total(conn, cart_id):
    total_row = conn.execute("""
        SELECT COALESCE(SUM(menu_items.price * cart_items.quantity), 0) AS total
        FROM cart_items
        JOIN menu_items ON cart_items.menu_item_id = menu_items.id
        WHERE cart_items.cart_id = ?
    """, (cart_id,)).fetchone()

    return total_row["total"]


def get_or_create_cart(conn, session_id):
    cart = conn.execute(
        "SELECT id FROM carts WHERE session_id = ?",
        (session_id,)
    ).fetchone()

    if cart is not None:
        return cart["id"]

    cursor = conn.execute(
        "INSERT INTO carts (session_id) VALUES (?)",
        (session_id,)
    )

    return cursor.lastrowid


def add_to_cart(session_id, item_id, quantity):
    if session_id is None:
        return {"error": "Session ID is required"}

    if item_id is None:
        return {"error": "Item ID is required"}

    if quantity is None:
        return {"error": "Quantity is required"}

    if quantity < 1:
        return {"error": "Quantity must be at least 1"}

    if quantity > 20:
        return {"error": "Quantity exceeds the maximum allowed limit"}

    with get_connection() as conn:
        item = conn.execute("""
            SELECT id, name, price, is_available
            FROM menu_items
            WHERE id = ?
        """, (item_id,)).fetchone()

        if item is None:
            return {"error": "Invalid item ID"}

        if item["is_available"] == 0:
            return {"error": "This item is currently unavailable."}

        cart_id = get_or_create_cart(conn, session_id)

        conn.execute("""
            INSERT INTO cart_items (cart_id, menu_item_id, quantity)
            VALUES (?, ?, ?)
        """, (cart_id, item_id, quantity))

        cart_total = calculate_cart_total(conn, cart_id)

        return {
            "message": "Item added to cart",
            "cart_total": cart_total
        }


def remove_from_cart(session_id, item_id):
    if session_id is None:
        return {"error": "Session ID is required"}

    if item_id is None:
        return {"error": "Item ID is required"}

    with get_connection() as conn:
        cart = conn.execute(
            "SELECT id FROM carts WHERE session_id = ?",
            (session_id,)
        ).fetchone()

        if cart is None:
            return {"error": "Cart not found"}

        cart_id = cart["id"]

        conn.execute(
            "DELETE FROM cart_items WHERE cart_id = ? AND menu_item_id = ?",
            (cart_id, item_id)
        )

        cart_total = calculate_cart_total(conn, cart_id)

        return {
            "message": "Item removed from cart",
            "cart_total": cart_total
        }