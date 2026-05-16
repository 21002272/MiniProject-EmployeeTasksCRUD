from flask import Blueprint, request, jsonify
from models import db, Employee

employees_bp = Blueprint("employees", __name__)

@employees_bp.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"message": "Invalid data"}), 400
    employee = Employee(name=data["name"], email=data["email"])
    db.session.add(employee)
    db.session.commit()
    return jsonify({"message": "Employee created successfully", "employee": employee.to_dict()}), 201

@employees_bp.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    if not employees:
        return jsonify({"message": "No employees found"})
    return jsonify({"message": "Employees retrieved successfully", "employees": [e.to_dict() for e in employees]})

@employees_bp.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({
        "message": "Employee retrieved successfully",
        "employee": employee.to_dict()
    })

@employees_bp.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    employee.name = data.get("name", employee.name)
    employee.email = data.get("email", employee.email)
    db.session.commit()
    return jsonify({"message": "Employee updated successfully", "employee": employee.to_dict()})

@employees_bp.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"})
