from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()

# ---------- ROUTES ----------
@app.route("/")
def ui():
    return render_template("index.html")

# ✅ ADD + GET students
@app.route("/students", methods=["GET", "POST"])
def students():
    conn = get_db_connection()

    if request.method == "POST":
        data = request.json
        conn.execute(
            "INSERT INTO students (name, course) VALUES (?, ?)",
            (data["name"], data["course"])
        )
        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Student added successfully"
        })

    # GET
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    students = [dict(row) for row in rows]

    return jsonify({
        "status": "success",
        "students": students
    })

# ✅ UPDATE
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "UPDATE students SET name=?, course=? WHERE id=?",
        (data["name"], data["course"], id)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Student updated"})

# ✅ DELETE
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Student deleted"})

if __name__ == "__main__":
    app.run(debug=True)

