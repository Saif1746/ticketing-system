from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = "tickets.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create")
def create_ticket_page():
    return render_template("create_ticket.html")


@app.route("/create", methods=["POST"])
def create_ticket():
    subject = request.form.get("subject")
    description = request.form.get("description")

    if not subject or not description:
        return "Subject and description are required"

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tickets (subject, description) VALUES (?, ?)",
        (subject, description)
    )
    conn.commit()
    conn.close()
    return redirect("/tickets")


@app.route("/tickets")
def tickets():
    conn = get_db_connection()
    ticket_list = conn.execute(
        "SELECT * FROM tickets ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("tickets.html", tickets=ticket_list)


@app.route("/admin")
def admin():
    conn = get_db_connection()
    ticket_list = conn.execute(
        "SELECT * FROM tickets ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("admin.html", tickets=ticket_list)


@app.route("/admin/update/<int:ticket_id>", methods=["POST"])
def update_status(ticket_id):
    status = request.form.get("status")
    allowed_status = ["Open", "In Progress", "Resolved"]

    if status not in allowed_status:
        return "Invalid status"

    conn = get_db_connection()
    conn.execute(
        "UPDATE tickets SET status = ? WHERE id = ?",
        (status, ticket_id)
    )
    conn.commit()
    conn.close()
    return redirect("/admin")


@app.route("/admin/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM tickets WHERE id = ?",
        (ticket_id,)
    )
    conn.commit()
    conn.close()
    return redirect("/admin")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)
