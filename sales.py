
import sqlite3
from datetime import datetime

DB_NAME = "kirana.db"


def record_sale(product, quantity, price, order_id=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    total = quantity * price

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER UNIQUE,
            product TEXT,
            quantity REAL,
            price REAL,
            total REAL,
            date TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(sales)")
    columns = [row[1] for row in cursor.fetchall()]

    if "order_id" not in columns:
        cursor.execute("ALTER TABLE sales ADD COLUMN order_id INTEGER")

    cursor.execute("""
        INSERT INTO sales (order_id, product, quantity, price, total, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        order_id,
        product,
        quantity,
        price,
        total,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return total

def get_daily_sales():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT SUM(total), COUNT(*)
        FROM sales
        WHERE date LIKE ?
    """, (today + "%",))

    result = cursor.fetchone()
    conn.close()

    total_sales = result[0] or 0
    number_of_sales = result[1] or 0

    print(f"Total sales today: ₹{total_sales}")
    print(f"Number of sales: {number_of_sales}")

    return total_sales, number_of_sales
