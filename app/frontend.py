from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
API_BASE = "http://api:5000"

@app.route("/")
def home():
    priority = request.args.get("priority")
    params = {"priority": priority} if priority else {}
    response = requests.get(f"{API_BASE}/todos", params=params)
    todos = response.json()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form["task"]
    priority = request.form["priority"]
    date = request.form["date"]
    requests.post(f"{API_BASE}/todos", json={"task": task, "priority": priority, "date": date})
    return redirect("/")

@app.route("/delete/<todo_id>")
def delete_todo(todo_id):
    requests.delete(f"{API_BASE}/todos/{todo_id}")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

