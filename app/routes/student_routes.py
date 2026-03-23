from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
import asyncio

from app.errors.exceptions import ResourceNotFoundError, ValidationError
from app.schemas.student_schema import StudentCreate
from app.services.student_service import (
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student
)
from app.db.database import AsyncSessionLocal
from app.db.models import Student
from sqlalchemy.future import select

student_bp = Blueprint("students", __name__)

# --- UI Routes ---

@student_bp.route("/")
def index():
    students = asyncio.run(get_students())
    return render_template("index.html", students=students)


@student_bp.route("/student/<int:id>")
def view_student(id):
    student = asyncio.run(get_student(id))
    if not student:
        raise ResourceNotFoundError("Student not found")
    return render_template("view_student.html", student=student)


@student_bp.route("/add", methods=["GET", "POST"])
def add_student_view():
    if request.method == "POST":
        try:
            data = StudentCreate(
                name=request.form.get("name"),
                email=request.form.get("email"),
                age=int(request.form.get("age")),
                course=request.form.get("course")
            )
            asyncio.run(create_student(data))
            flash("Student added successfully!", "success")
            return redirect(url_for("students.index"))
        except ValueError as e:
            raise ValidationError(f"Invalid input: {str(e)}")
    
    return render_template("add_student.html")


@student_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student_view(id):
    student = asyncio.run(get_student(id))
    if not student:
        raise ResourceNotFoundError("Student not found")

    if request.method == "POST":
        try:
            data = StudentCreate(
                name=request.form.get("name"),
                email=request.form.get("email"),
                age=int(request.form.get("age")),
                course=request.form.get("course")
            )
            asyncio.run(update_student(id, data))
            flash("Student updated successfully!", "success")
            return redirect(url_for("students.index"))
        except ValueError as e:
            raise ValidationError(f"Invalid input: {str(e)}")

    return render_template("edit_student.html", student=student)


# --- API Routes (JSON) ---

@student_bp.route("/api/students", methods=["POST"])
def add_student_api():
    data = StudentCreate(**request.json)
    student = asyncio.run(create_student(data))
    return jsonify({"message": "Student created", "data": student.id})


@student_bp.route("/api/students", methods=["GET"])
def get_all_students_api():
    students = asyncio.run(get_students())
    return jsonify([s.__dict__ for s in students if not s.__dict__.pop('_sa_instance_state', None)])


@student_bp.route("/api/students/<int:id>", methods=["PUT"])
def update_api(id):
    data = StudentCreate(**request.json)
    student = asyncio.run(update_student(id, data))

    if not student:
        raise ResourceNotFoundError("Student not found")

    return jsonify({"message": "Updated"})


@student_bp.route("/api/students/<int:id>", methods=["DELETE"])
def delete_api(id):
    student = asyncio.run(delete_student(id))

    if not student:
        raise ResourceNotFoundError("Student not found")

    return jsonify({"message": "Deleted"})
