import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DB_PATH = "learning_log.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # så du kan skrive row["topic"]
    return conn


def init_db():
    with get_db() as conn:
        # TODO 1: Opret tabellen 'logs' hvis den ikke findes.
        # Kolonner: id, date, topic, minutes, notes 
        conn.execute("""
	 CREATE TABLE IF NOT EXISTS logs (
		id      INTEGER PRIMARY KEY AUTOINCREMENT,
                date    TEXT,
                topic   TEXT,
                minutes INTEGER,
                notes   TEXT
            )
        """)


@app.route("/")
def index():
    with get_db() as conn:
        # TODO 2: Hent alle logs, nyeste først
        logs = conn.execute("SELECT * FROM logs ORDER BY date DESC, id DESC").fetchall()
    return render_template("index.html", logs=logs)


@app.route("/add", methods=["POST"])
def add():
    topic = request.form["topic"]
    minutes = int(request.form["minutes"])
    notes = request.form.get("notes", "")
    today = date.today().isoformat()

    with get_db() as conn:
        # TODO 3: Indsæt en ny række. Brug ? som pladsholdere
        conn.execute("INSERT INTO logs (date, topic, minutes, notes) VALUES (?, ?, ?, ?)",
		    (today, topic, minutes, notes )
)
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
