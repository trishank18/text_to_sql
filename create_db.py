"""Create and seed the sample sales SQLite database."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("sales.db")


def create_database() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                city TEXT
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL REFERENCES customers(id),
                product TEXT NOT NULL,
                amount REAL NOT NULL,
                order_date TEXT NOT NULL
            );
            """
        )
        connection.executemany(
            "INSERT OR REPLACE INTO customers (id, name, email, city) VALUES (?, ?, ?, ?)",
            [
                (1, "Aarav Sharma", "aarav.sharma@example.com", "Mumbai"),
                (2, "Priya Verma", "priya.verma@example.com", "Delhi"),
                (3, "Rohan Patel", "rohan.patel@example.com", "Bangalore"),
                (4, "Ananya Iyer", "ananya.iyer@example.com", "Chennai"),
                (5, "Vikram Reddy", "vikram.reddy@example.com", "Hyderabad"),
            ],
        )
        connection.executemany(
            "INSERT OR REPLACE INTO orders (id, customer_id, product, amount, order_date) "
            "VALUES (?, ?, ?, ?, ?)",
            [
                (1, 1, "Laptop", 68999.00, "2026-01-12"),
                (2, 1, "Phone", 24999.00, "2026-01-18"),
                (3, 2, "Tablet", 32999.00, "2026-02-03"),
                (4, 2, "Phone", 18999.00, "2026-02-15"),
                (5, 3, "Laptop", 74999.00, "2026-03-01"),
                (6, 3, "Tablet", 27999.00, "2026-03-08"),
                (7, 4, "Phone", 31999.00, "2026-03-14"),
                (8, 4, "Laptop", 82999.00, "2026-03-20"),
                (9, 5, "Tablet", 35999.00, "2026-04-02"),
                (10, 5, "Phone", 22999.00, "2026-04-09"),
            ],
        )
    print(f"Database created and seeded successfully: {DB_PATH}")


if __name__ == "__main__":
    create_database()
