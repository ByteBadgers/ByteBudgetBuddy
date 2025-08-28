import sqlite3
from datetime import datetime
from io import StringIO
import csv

from flask import Flask, render_template, request, redirect, url_for, Response, flash

app = Flask(__name__)
app.secret_key = "secret123" 
DB = "finance.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK (type IN ('Income','Expense')),
                amount REAL NOT NULL,
                category TEXT,
                date TEXT NOT NULL
            )
        """)

def add_transaction(t_type, amount, category):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "INSERT INTO transactions (type, amount, category, date) VALUES (?,?,?,?)",
            (t_type, float(amount), category.strip() or "Uncategorized",
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

def fetch_all():
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(
            "SELECT * FROM transactions ORDER BY datetime(date) DESC, id DESC"
        ).fetchall()

def get_summary():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        income = cur.execute(
            "SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='Income'"
        ).fetchone()[0] or 0
        expenses = cur.execute(
            "SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='Expense'"
        ).fetchone()[0] or 0
    return {"income": income, "expenses": expenses, "balance": income - expenses}

def get_breakdown():
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(
            "SELECT category, COALESCE(SUM(amount),0) AS total "
            "FROM transactions WHERE type='Expense' "
            "GROUP BY category ORDER BY total DESC"
        ).fetchall()

@app.route("/")
def index():
    init_db()
    summary = get_summary()
    breakdown = get_breakdown()
    recent = fetch_all()[:10]

    return render_template(
        "index.html",
        summary=summary,
        breakdown=breakdown,
        recent=recent
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    init_db()
    if request.method == "POST":
        t_type = request.form.get("type")
        amount = request.form.get("amount", type=float)
        category = request.form.get("category", "")
        if t_type in ("Income", "Expense") and amount is not None:
            add_transaction(t_type, amount, category)
            flash("✅ Transaction added successfully!", "success")
        else:
            flash("⚠️ Invalid transaction data.", "error")
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/transactions")
def transactions():
    rows = fetch_all()
    return render_template("transactions.html", rows=rows)

@app.route("/export.csv")
def export_csv():
    rows = fetch_all()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["ID", "Type", "Amount", "Category", "Date"])
    for r in rows:
        writer.writerow([r["id"], r["type"], r["amount"], r["category"], r["date"]])
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
