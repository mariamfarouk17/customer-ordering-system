# services/order_service.py
# Handles order creation and retrieval for the Customer Ordering System.

from datetime import datetime
from models.database import get_connection
from services.payment_simulator import process_payment


def create_order(session_id, order_type, payment_method, table_number=None, pickup_time=None):
    """
    Creates a new order from the user's current cart.

    Steps:
    1. Validate inputs.
    2. Process payment simulation.
    3. Find the cart and its items.
    4. Check item availability.
    5. Calculate totals.
    6. Insert order and order items into the database.
    7. Clear the cart.
    8. Return order summary.
    """

    # --- Validation ---

    if not session_id:
        return {"error": "Session ID is required", "status_code": 400}

    if order_type not in ("Dine-In", "Takeaway"):
        return {"error": "order_type must be 'Dine-In' or 'Takeaway'", "status_code": 400}

    if order_type == "Dine-In" and not table_number:
        return {"error": "table_number is required for Dine-In orders", "status_code": 400}

    if order_type == "Takeaway" and not pickup_time:
        return {"error": "pickup_time is required for Takeaway orders", "status_code": 400}

    # Simulate payment before doing any database work
    payment_result = process_payment(payment_method)
    if not payment_result["success"]:
        return {"error": payment_result["error"], "status_code": 400}

    with get_connection() as conn:
        cursor = conn.cursor()

        # --- Find the cart by session_id ---
        cursor.execute(
            "SELECT id FROM carts WHERE session_id = ?",
            (session_id,)
        )
        cart_row = cursor.fetchone()

        if not cart_row:
            return {"error": "Cart not found", "status_code": 404}

        cart_id = cart_row[0]

        # --- Get cart items joined with menu item details ---
        cursor.execute(
            """
            SELECT
                ci.menu_item_id,
                mi.name,
                mi.price,
                ci.quantity,
                mi.is_available
            FROM cart_items ci
            JOIN menu_items mi ON ci.menu_item_id = mi.id
            WHERE ci.cart_id = ?
            """,
            (cart_id,)
        )
        cart_items = cursor.fetchall()

        if not cart_items:
            return {"error": "Cart is empty", "status_code": 400}

        # --- Check availability of all items ---
        unavailable = [row[1] for row in cart_items if row[4] == 0]
        if unavailable:
            return {
                "error": "Some items are no longer available.",
                "unavailable_items": unavailable,
                "status_code": 422
            }

        # --- Calculate pricing ---
        subtotal = sum(row[2] * row[3] for row in cart_items)  # price * quantity
        promo_code = None
        discount_amount = 0
        total = subtotal

        # --- Insert the order into the orders table ---
        created_at = datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO orders (
                order_code, order_type, table_number, pickup_time,
                payment_method, status, subtotal, promo_code,
                discount_amount, total, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "",  # placeholder; we'll update after getting the real id
                order_type,
                table_number,
                pickup_time,
                payment_method,
                "Pending",
                subtotal,
                promo_code,
                discount_amount,
                total,
                created_at
            )
        )

        # Get the newly created order's ID
        order_id = cursor.lastrowid

        # Generate order_code using the order ID (e.g., ORD-00001)
        order_code = f"ORD-{order_id:05d}"

        # Update the order row with the generated order_code
        cursor.execute(
            "UPDATE orders SET order_code = ? WHERE id = ?",
            (order_code, order_id)
        )

        # --- Insert each cart item into order_items ---
        for item in cart_items:
            menu_item_id = item[0]
            unit_price = item[2]
            quantity = item[3]

            cursor.execute(
                """
                INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
                """,
                (order_id, menu_item_id, quantity, unit_price)
            )

        # --- Clear the cart after successful order ---
        cursor.execute(
            "DELETE FROM cart_items WHERE cart_id = ?",
            (cart_id,)
        )

        conn.commit()

    # --- Return order summary ---
    return {
        "message": "Order created successfully",
        "order_code": order_code,
        "status": "Pending",
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "total": total
    }


def get_order_by_code(order_code):
    """
    Retrieves a full order summary by order_code,
    including the list of ordered items.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        # --- Find the order ---
        cursor.execute(
            """
            SELECT
                order_code, status, order_type, table_number,
                pickup_time, payment_method, subtotal,
                discount_amount, total, created_at
            FROM orders
            WHERE order_code = ?
            """,
            (order_code,)
        )
        order_row = cursor.fetchone()

        if not order_row:
            return {"error": "Order not found"}

        # Map columns to a readable dictionary
        order = {
            "order_code":      order_row[0],
            "status":          order_row[1],
            "order_type":      order_row[2],
            "table_number":    order_row[3],
            "pickup_time":     order_row[4],
            "payment_method":  order_row[5],
            "subtotal":        order_row[6],
            "discount_amount": order_row[7],
            "total":           order_row[8],
            "created_at":      order_row[9],
        }

        # --- Get the items for this order ---
        cursor.execute(
            """
            SELECT
                mi.name,
                oi.quantity,
                oi.unit_price
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = (
                SELECT id FROM orders WHERE order_code = ?
            )
            """,
            (order_code,)
        )
        item_rows = cursor.fetchall()

        order["items"] = [
            {
                "name":       row[0],
                "quantity":   row[1],
                "unit_price": row[2]
            }
            for row in item_rows
        ]

    return order