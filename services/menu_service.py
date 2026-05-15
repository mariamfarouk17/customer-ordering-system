from models.database import get_connection


def get_all_items():
    """
    Returns all menu items grouped by category.

    Example return value:
    {
        "categories": [
            {
                "name": "Wraps",
                "items": [
                    { "id": 1, "name": "Chicken Shawarma", "price": 6.50, "is_available": True }
                ]
            }
        ]
    }
    """
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, category, price, is_available FROM menu_items ORDER BY category, name"
        ).fetchall()

    # Group items by category using a plain dictionary
    # Keys are category names, values are lists of item dicts
    grouped = {}

    for row in rows:
        category = row["category"]

        # Create a new category list the first time we see this category
        if category not in grouped:
            grouped[category] = []

        grouped[category].append({
            "id":           row["id"],
            "name":         row["name"],
            "price":        row["price"],
            # SQLite stores booleans as 0/1 integers; convert to Python bool
            "is_available": bool(row["is_available"])
        })

    # Build the final list of category objects in the required format
    categories = [
        {"name": category_name, "items": items}
        for category_name, items in grouped.items()
    ]

    return {"categories": categories}


def get_item_by_id(item_id):
    """
    Returns a single menu item as a dict, or None if it does not exist.

    Parameters:
        item_id (int): The id of the menu item to look up.
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, category, price, is_available FROM menu_items WHERE id = ?",
            (item_id,)
        ).fetchone()

    # fetchone() returns None when no row is found
    if row is None:
        return None

    return {
        "id":           row["id"],
        "name":         row["name"],
        "category":     row["category"],
        "price":        row["price"],
        "is_available": bool(row["is_available"])
    }


def is_item_available(item_id):
    """
    Returns True if the item exists and is currently available.
    Returns False if the item does not exist or is marked unavailable.

    Parameters:
        item_id (int): The id of the menu item to check.
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT is_available FROM menu_items WHERE id = ?",
            (item_id,)
        ).fetchone()

    # Item not found in the database
    if row is None:
        return False

    return row["is_available"] == 1


def update_item(item_id, data):
    """
    Updates a menu item's price and/or availability.
    Only the fields provided in `data` are updated — nothing else is touched.

    Returns True if the item was found and updated.
    Returns False if the item does not exist.

    Parameters:
        item_id (int): The id of the menu item to update.
        data    (dict): A dict with optional keys: "price", "is_available".

    Example:
        update_item(1, {"price": 7.00})
        update_item(1, {"is_available": 0})
        update_item(1, {"price": 7.00, "is_available": 1})
    """
    # Make sure the item actually exists before trying to update it
    if get_item_by_id(item_id) is None:
        return False

    # Build the SET clause dynamically based on what was provided.
    # This avoids overwriting fields the caller did not mention.
    fields = []   # e.g. ["price = ?", "is_available = ?"]
    values = []   # matching values for the ? placeholders

    if "price" in data:
        fields.append("price = ?")
        values.append(data["price"])

    if "is_available" in data:
        fields.append("is_available = ?")
        values.append(data["is_available"])

    # Nothing recognised in data — nothing to do
    if not fields:
        return False

    # Append item_id at the end to match the WHERE clause placeholder
    values.append(item_id)

    sql = f"UPDATE menu_items SET {', '.join(fields)} WHERE id = ?"

    with get_connection() as conn:
        conn.execute(sql, values)

    return True
