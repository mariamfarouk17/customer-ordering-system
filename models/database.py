import sqlite3

# The name of the SQLite database file
DB_NAME = "cos.db"


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    - detect_types allows SQLite to return Python-native types.
    - The connection can be used as a context manager (with statement),
      which automatically commits on success or rolls back on error.
    """
    conn = sqlite3.connect(DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES)

    # Return rows as dict-like objects so we can access columns by name
    # e.g. row["name"] instead of row[0]
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    """
    Creates all database tables if they do not already exist.
    Safe to run multiple times — it will never overwrite existing data.
    """
    with get_connection() as conn:

        # Menu items available for ordering
        conn.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT    NOT NULL,
                category     TEXT    NOT NULL,
                price        REAL    NOT NULL,
                is_available INTEGER NOT NULL DEFAULT 1
            )
        """)

        # Promo codes customers can apply at checkout
        conn.execute("""
            CREATE TABLE IF NOT EXISTS promo_codes (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                code             TEXT    NOT NULL UNIQUE,
                discount_percent REAL    NOT NULL,
                is_active        INTEGER NOT NULL DEFAULT 1
            )
        """)

        # One cart per customer session
        conn.execute("""
            CREATE TABLE IF NOT EXISTS carts (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT    NOT NULL
            )
        """)

        # Individual items inside a cart
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                cart_id      INTEGER NOT NULL,
                menu_item_id INTEGER NOT NULL,
                quantity     INTEGER NOT NULL,
                FOREIGN KEY (cart_id)      REFERENCES carts(id),
                FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
            )
        """)

        # A completed order created after successful checkout
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                order_code     TEXT    NOT NULL UNIQUE,
                order_type     TEXT    NOT NULL,
                table_number   TEXT,
                pickup_time    TEXT,
                payment_method TEXT    NOT NULL,
                status         TEXT    NOT NULL DEFAULT 'Pending',
                subtotal       REAL    NOT NULL,
                promo_code     TEXT,
                discount_amount REAL   DEFAULT 0,
                total          REAL    NOT NULL,
                created_at     TEXT    NOT NULL
            )
        """)

        # The individual menu items that belong to an order
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id     INTEGER NOT NULL,
                menu_item_id INTEGER NOT NULL,
                quantity     INTEGER NOT NULL,
                unit_price   REAL    NOT NULL,
                FOREIGN KEY (order_id)     REFERENCES orders(id),
                FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
            )
        """)


def seed_data():
    """
    Inserts sample menu items and promo codes into the database.
    Only runs if the tables are currently empty, so existing data is never duplicated.
    """
    with get_connection() as conn:

        # --- Seed menu items ---
        existing_items = conn.execute("SELECT COUNT(*) FROM menu_items").fetchone()[0]

        if existing_items == 0:
            sample_items = [
                # (name, category, price, is_available)
                ("Chicken Shawarma", "Wraps",  6.50, 1),
                ("Falafel Wrap",     "Wraps",  5.50, 1),
                ("Cola",             "Drinks", 1.50, 1),
                ("Fries",            "Sides",  2.00, 0),  # currently unavailable
            ]

            conn.executemany(
                "INSERT INTO menu_items (name, category, price, is_available) VALUES (?, ?, ?, ?)",
                sample_items
            )

        # --- Seed promo codes ---
        existing_promos = conn.execute("SELECT COUNT(*) FROM promo_codes").fetchone()[0]

        if existing_promos == 0:
            sample_promos = [
                # (code, discount_percent, is_active)
                ("SAVE10",    10.0, 1),  # 10% off, active
                ("STUDENT15", 15.0, 1),  # 15% off, active
                ("EXPIRED20", 20.0, 0),  # 20% off, inactive
            ]

            conn.executemany(
                "INSERT INTO promo_codes (code, discount_percent, is_active) VALUES (?, ?, ?)",
                sample_promos
            )


# Run this file directly to set up the database for the first time:
#   python models/database.py
if __name__ == "__main__":
    init_db()
    seed_data()
    print("Database initialized successfully.")