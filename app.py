
from flask import Flask, render_template, request, redirect
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "studentuser"),
        password=os.getenv("MYSQL_PASSWORD", "studentpass123"),
        database=os.getenv("MYSQL_DATABASE", "studentdb")
    )

def initialize_database():
    for attempt in range(10):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    course VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("Database connected successfully!")
            return
        except mysql.connector.Error as error:
            print(f"Database connection attempt {attempt + 1}: {error}")
            time.sleep(5)

    raise RuntimeError("Could not connect to MySQL.")

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"].strip()
    course = request.form["course"].strip()
    email = request.form["email"].strip()

    if name and course and email:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, email) VALUES (%s, %s, %s)",
            (name, course, email)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect("/")

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=False)
