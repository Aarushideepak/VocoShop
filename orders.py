
import sqlite3
from datetime import datetime
from inventory import increase_stock

DB_NAME = "kirana.db"


def create_order(product, quantity, price):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            quantity REAL,
            price REAL,
            total REAL,
            status TEXT,
            date TEXT
        )
    """)

    total = quantity * price

    cursor.execute("""
        INSERT INTO orders
        (product, quantity, price, total, status, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product,
        quantity,
        price,
        total,
        "Confirmed",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    order_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    return order_id, total


def show_orders():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, product, quantity, price, total, status, date
        FROM orders
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()
    conn.close()

    if not orders:
        print("No orders found.")
        return

    print("\n===== ORDER HISTORY =====")

    for order in orders:
        print(f"""
Order ID: {order[0]}
Product: {order[1]}
Quantity: {order[2]}
Price: ₹{order[3]}
Total: ₹{order[4]}
Status: {order[5]}
Date: {order[6]}
-------------------------
""")


def cancel_order(order_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT product, quantity, status FROM orders WHERE id = ?",
        (order_id,)
    )

    order = cursor.fetchone()

    if not order:
        print("Order not found.")
        conn.close()
        return

    product, quantity, status = order

    if status == "Cancelled":
        print("This order is already cancelled.")
        conn.close()
        return

    cursor.execute(
        "UPDATE orders SET status = 'Cancelled' WHERE id = ?",
        (order_id,)
    )
    cursor.execute(
    "DELETE FROM sales WHERE order_id = ?",
    (order_id,)
)
    conn.commit()
    conn.close()

    increase_stock(product, quantity)

    print(f"Order {order_id} cancelled successfully.")
    print(f"{quantity} units of {product} restored to stock.")
