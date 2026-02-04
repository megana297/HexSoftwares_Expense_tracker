from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "expenses.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create table
conn = get_db_connection()
conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    )
""")
conn.commit()
conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_expense():
    data = request.get_json()

    category = data.get("category")
    amount = data.get("amount")
    description = data.get("description")

    if not category or not amount:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (category, amount, description) VALUES (?, ?, ?)",
        (category, float(amount), description)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"})

@app.route("/expenses", methods=["GET"])
def get_expenses():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    return jsonify([dict(exp) for exp in expenses])

if __name__ == "__main__":
    app.run(debug=True)
