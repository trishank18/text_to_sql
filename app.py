"""Flask web application for the text-to-SQL database assistant."""

from flask import Flask, render_template, request

from text_to_sql import SCHEMA, generate_sql, run_query

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    sql = None
    columns = []
    rows = []
    error = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if not question:
            error = "Enter a question before searching."
        else:
            try:
                sql = generate_sql(question)
                columns, rows = run_query(sql)
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"

    return render_template(
        "index.html",
        question=question,
        schema=SCHEMA,
        sql=sql,
        columns=columns,
        rows=rows,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
