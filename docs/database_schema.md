CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0),
    is_available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE promo_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    discount_percent REAL NOT NULL CHECK(discount_percent > 0 AND discount_percent <= 100),
    expiry_date TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE carts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity >= 1 AND quantity <= 20),

    FOREIGN KEY (cart_id) REFERENCES carts(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_code TEXT NOT NULL UNIQUE,
    idempotency_key TEXT UNIQUE,
    session_id TEXT NOT NULL,

    order_type TEXT NOT NULL CHECK(order_type IN ('Dine-In', 'Takeaway')),
    table_number TEXT,
    pickup_time TEXT,

    payment_method TEXT NOT NULL CHECK(payment_method IN ('Cash', 'Mock Card')),
    payment_status TEXT NOT NULL DEFAULT 'Pending' CHECK(payment_status IN ('Pending', 'Paid', 'Failed')),

    status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Confirmed', 'Cancelled')),

    subtotal REAL NOT NULL CHECK(subtotal >= 0),
    promo_code TEXT,
    discount_amount REAL DEFAULT 0 CHECK(discount_amount >= 0),
    total REAL NOT NULL CHECK(total >= 0),

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity >= 1 AND quantity <= 20),
    unit_price REAL NOT NULL CHECK(unit_price > 0),

    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);
