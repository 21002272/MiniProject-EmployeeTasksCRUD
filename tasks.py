from flask import Blueprint, request, jsonify
from models import db, Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data or "status" not in data or "employee_id" not in data:
        return jsonify({"message": "Invalid data"}), 400
    task = Task(title=data["title"], status=data["status"], employee_id=data["employee_id"])
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created successfully", "task": task.to_dict()}), 201

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    if not tasks:
        return jsonify({"message": "No tasks found"})
    return jsonify({"message": "Tasks retrieved successfully", "tasks": [t.to_dict() for t in tasks]})

@tasks_bp.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({
        "message": "Task retrieved successfully",
        "task": task.to_dict()
    })

@tasks_bp.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.status = data.get("status", task.status)
    task.employee_id = data.get("employee_id", task.employee_id)
    db.session.commit()
    return jsonify({"message": "Task updated successfully", "task": task.to_dict()})

@tasks_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})
