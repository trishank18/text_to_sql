"""Interactive console for asking natural-language questions about the database."""

import sys

from text_to_sql import SCHEMA, generate_sql, print_table, run_query

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


def color(text: str, color_code: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"{color_code}{text}{RESET}"


def main() -> None:
    print(color("\nText-to-SQL console (Gemini + SQLite)", CYAN))
    print("Commands: schema (show tables), quit or exit (close the console)\n")
    print(color("Database schema:", CYAN))
    print(SCHEMA)

    while True:
        try:
            question = input("Enter your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        command = question.lower()
        if command in {"quit", "exit"}:
            print("Goodbye!")
            break
        if command == "schema":
            print(color("\nDatabase schema:", CYAN))
            print(SCHEMA)
            continue
        if not question:
            continue

        print(color("Generating SQL with Gemini...", CYAN), flush=True)
        try:
            sql = generate_sql(question)
            columns, rows = run_query(sql)
            print(color(f"\nSQL: {sql}", GREEN))
            if rows:
                print_table(columns, rows)
                print(color(f"{len(rows)} row(s) returned.\n", GREEN))
            else:
                print(color("Query succeeded; no rows found.\n", GREEN))
        except Exception as exc:
            print(color(f"Error: {type(exc).__name__}: {exc}", RED))
            print(color("Check GEMINI_API_KEY, your internet connection, and the database.\n", RED))


if __name__ == "__main__":
    main()
