
import sqlite3

def create_database():
    connection = sqlite3.connect("kirana.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT UNIQUE,
            quantity REAL,
            unit TEXT,
            price REAL
        )
    """)

    connection.commit()
    connection.close()

    print("Kirana inventory database created!")

if __name__ == "__main__":
    create_database()
