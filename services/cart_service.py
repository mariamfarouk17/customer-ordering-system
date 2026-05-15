from models.database import get_connection


def add_to_cart(session_id, item_id, quantity):

    # --- 1. Validate quantity ---
    if quantity is None:
        return {"error": "Quantity is required"}
    if quantity < 1:
        return {"error": "Quantity must be at least 1"}
    if quantity > 20:
        return {"error": "Quantity exceeds the maximum allowed limit"}

    with get_connection() as conn:

        # --- 2. Validate menu item ---
        item = conn.execute(
            "SELECT id, is_available FROM menu_items WHERE id = ?",
            (item_id,)
        ).fetchone()

        if item is None:
            return {"error": "Invalid item ID"}
        if item["is_available"] == 0:
            return {"error": "This item is currently unavailable."}

        # --- 3. Find or create cart for this session ---
        cart = conn.execute(
            "SELECT id FROM carts WHERE session_id = ?",
            (session_id,)
        ).fetchone()

        if cart is None:
            cursor = conn.execute(
                "INSERT INTO carts (session_id) VALUES (?)",
                (session_id,)
            )
            cart_id = cursor.lastrowid
        else:
            cart_id = cart["id"]

        # --- 4. Insert the item into cart_items ---
        conn.execute(
            "INSERT INTO cart_items (cart_id, menu_item_id, quantity) VALUES (?, ?, ?)",
            (cart_id, item_id, quantity)
        )

        # --- 5. Calculate cart total from the database ---
        # Price always comes from menu_items — never trusted from the frontend
        row = conn.execute(
            """
            SELECT SUM(m.price * ci.quantity) AS total
            FROM cart_items ci
            JOIN menu_items m ON m.id = ci.menu_item_id
            WHERE ci.cart_id = ?
            """,
            (cart_id,)
        ).fetchone()

        cart_total = round(row["total"], 2) if row["total"] is not None else 0.0

    return {
        "message": "Item added to cart",
        "cart_total": cart_total
    }