from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Connect to Postgres using environment variables
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db"   # <- "db" is the service name from docker-compose
    )

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (description) VALUES (%s);", (task,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Task '{task}' added!"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, description FROM tasks;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "task": r[1]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

