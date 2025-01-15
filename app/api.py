from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/todos"
mongo = PyMongo(app)

@app.route("/todos", methods=["GET"])
def get_todos():
    priority = request.args.get("priority")
    date = request.args.get("date")
    todos = mongo.db.todos
    query = {}
    
    if priority:
        query["priority"] = priority
    
    if date:
        try:
            query["date"] = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    result = []
    for todo in todos.find(query):
        todo_data = {
            "_id": str(todo["_id"]),
            "task": todo["task"],
            "priority": todo["priority"],
            "date": todo["date"]
        }
        if isinstance(todo["date"], datetime):
            todo_data["date"] = todo["date"].strftime("%Y-%m-%d")
        result.append(todo_data)
    
    return jsonify(result)

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    todo_id = mongo.db.todos.insert_one(data).inserted_id
    return jsonify({"_id": str(todo_id)}), 201

@app.route("/todos/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    mongo.db.todos.delete_one({"_id": ObjectId(todo_id)})
    return jsonify({"message": "Todo deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
