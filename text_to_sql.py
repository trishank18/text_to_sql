"""Turn a natural-language question into a read-only SQLite query with Gemini."""

import os
import re
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sales.db"
SCHEMA = """
customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
)
orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product TEXT,
    amount REAL,
    order_date TEXT
)
""".strip()

def generate_sql(question: str) -> str:
    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        raise RuntimeError("Add your Gemini API key to the GEMINI_API_KEY entry in .env")

    client = genai.Client(api_key=api_key)
    response = client.interactions.create(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        system_instruction=(
            "You are an expert SQLite analyst. Generate exactly one read-only "
            "SELECT query using only the provided schema. Return ONLY SQL, "
            "with no markdown or explanation. Never generate write statements. "
            "Always include LIMIT 50.\n\n"
            f"Schema:\n{SCHEMA}"
        ),
        input=question,
    )
    sql = (response.output_text or "").strip()
    sql = sql.removeprefix("```sql").removesuffix("```").strip()
    if not sql:
        raise ValueError("Gemini returned an empty response. Try the question again.")
    if not re.match(r"(?is)^select\b", sql) or re.search(r";\s*\S", sql):
        raise ValueError("The model did not return one SELECT query.")
    if not re.search(r"(?is)\blimit\s+\d+\s*$", sql.rstrip("; ")):
        sql = sql.rstrip("; ") + " LIMIT 50"
    return sql


def run_query(sql: str) -> tuple[list[str], list[tuple]]:
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run `python create_db.py` first.")
    connection = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    try:
        connection.set_authorizer(
            lambda action, _arg1, _arg2, _db, _source: (
                sqlite3.SQLITE_OK
                if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION)
                else sqlite3.SQLITE_DENY
            )
        )
        cursor = connection.execute(sql)
        columns = [description[0] for description in cursor.description or []]
        return columns, cursor.fetchall()
    finally:
        connection.close()


def print_table(columns: list[str], rows: list[tuple]) -> None:
    if not columns:
        print("Query completed; no columns to display.")
        return

    values = [["" if value is None else str(value) for value in row] for row in rows]
    widths = [
        max([len(str(column))] + [len(row[index]) for row in values])
        for index, column in enumerate(columns)
    ]
    border = "+-" + "-+-".join("-" * width for width in widths) + "-+"

    def format_row(row: list[str]) -> str:
        return "| " + " | ".join(value.ljust(widths[i]) for i, value in enumerate(row)) + " |"

    print(border)
    print(format_row([str(column) for column in columns]))
    print(border)
    for row in values:
        print(format_row(row))
    print(border)
