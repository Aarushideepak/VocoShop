
import sqlite3
from speech import speak
def add_product(product, quantity, unit, price):
    connection = sqlite3.connect("kirana.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO inventory (product, quantity, unit, price)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(product) DO UPDATE SET
        quantity = excluded.quantity,
        unit = excluded.unit,
        price = excluded.price
    """, (product.lower(), quantity, unit, price))

    connection.commit()
    connection.close()

    print(f"{product} added successfully!")


def show_inventory():
    connection = sqlite3.connect("kirana.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM inventory")
    products = cursor.fetchall()

    print("\n----- KIRANA INVENTORY -----")

    for item in products:
        print(
            f"{item[1]} | Stock: {item[2]} {item[3]} "
            f"| Price: Rs.{item[4]}"
        )

    connection.close()


def check_stock(product):
    connection = sqlite3.connect("kirana.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT quantity, unit, price FROM inventory WHERE product = ?",
        (product.lower(),)
    )

    result = cursor.fetchone()
    connection.close()

    if result:
        print(f"{product}: {result[0]} {result[1]} available")
        print(f"Price: Rs.{result[2]} per {result[1]}")
    else:
        print(f"{product} not found in inventory.")


def reduce_stock(product, quantity):
    connection = sqlite3.connect("kirana.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT quantity FROM inventory WHERE product = ?",
        (product.lower(),)
    )

    result = cursor.fetchone()

    if result and result[0] >= quantity:
        cursor.execute(
            "UPDATE inventory SET quantity = quantity - ? WHERE product = ?",
            (quantity, product.lower())
        )
        print("Stock updated successfully!")
    elif result:
        print("Not enough stock available!")
    else:
        print("Product not found!")

    connection.commit()
    connection.close()

def increase_stock(product, quantity):
    connection = sqlite3.connect("kirana.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE inventory SET quantity = quantity + ? WHERE product = ?",
        (quantity, product.lower())
    )

    updated = cursor.rowcount

    connection.commit()
    connection.close()

    if updated:
        print(f"Added {quantity} units to {product}!")
    else:
        print(f"{product} not found in inventory.")
def get_product_details(product):
    connection = sqlite3.connect("kirana.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT quantity, unit, price FROM inventory WHERE product = ?",
        (product.lower(),)
    )

    result = cursor.fetchone()
    connection.close()

    return result

if __name__ == "__main__":
    add_product("rice", 20, "kg", 60)
    add_product("sugar", 15, "kg", 45)
    add_product("milk", 30, "packets", 30)
    add_product("oil", 10, "litres", 150)

    show_inventory()

    print("\nChecking rice stock:")
    check_stock("rice")

    print("\nReducing rice stock:")
    reduce_stock("rice", 2)

    print("\nUpdated inventory:")
    show_inventory()
def check_low_stock(threshold=5):
    connection = sqlite3.connect("kirana.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product, quantity, unit
        FROM inventory
        WHERE quantity <= ?
    """, (threshold,))

    products = cursor.fetchall()
    connection.close()

    if not products:
        message = "All products have sufficient stock."
        print(message)
        speak(message)
        return

    print("\n===== LOW STOCK ALERT =====")

    for product, quantity, unit in products:
        message = f"{product} ಸ್ಟಾಕ್ ಕಡಿಮೆಯಾಗಿದೆ. ಇನ್ನು {int(quantity)} {unit} ಮಾತ್ರ ಉಳಿದಿದೆ."
        print(message)
        speak(message)