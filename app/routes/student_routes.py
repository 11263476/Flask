from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash  # Import Flask utilities
import asyncio  # Import asyncio to run our async service functions

from app.errors.exceptions import ResourceNotFoundError, ValidationError  # Import our custom errors
from app.schemas.student_schema import StudentCreate  # Import the data validation schema
from app.services.student_service import (  # Import our business logic functions
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student
)

student_bp = Blueprint("students", __name__)  # Create a Blueprint for student-related routes

# --- UI Routes (For Browser) ---

@student_bp.route("/")  # Root route for the Student Dashboard
def index():
    students = asyncio.run(get_students())  # Fetch all students from the DB
    return render_template("index.html", students=students)  # Render the dashboard template


@student_bp.route("/student/<int:id>")  # Route to view a specific student's profile
def view_student(id):
    student = asyncio.run(get_student(id))  # Fetch student by ID
    if not student:  # If student isn't found, raise a 404 error
        raise ResourceNotFoundError("Student not found")
    return render_template("view_student.html", student=student)  # Show the profile template


@student_bp.route("/add", methods=["GET", "POST"])  # Route to add a new student
def add_student_view():
    if request.method == "POST":  # Check if the form was submitted
        try:
            # Validate form data using our Pydantic schema
            data = StudentCreate(
                name=request.form.get("name"),
                email=request.form.get("email"),
                age=int(request.form.get("age")),
                course=request.form.get("course")
            )
            asyncio.run(create_student(data))  # Save the new student to the DB
            flash("Student added successfully!", "success")  # Send a success message to the browser
            return redirect(url_for("students.index"))  # Redirect back to the dashboard
        except ValueError as e:  # Handle cases where age is not a number
            raise ValidationError(f"Invalid input: {str(e)}")
    
    return render_template("add_student.html")  # If GET request, show the empty add form


@student_bp.route("/edit/<int:id>", methods=["GET", "POST"])  # Route to edit existing students
def edit_student_view(id):
    student = asyncio.run(get_student(id))  # Fetch the student to be edited
    if not student:  # Raise error if student doesn't exist
        raise ResourceNotFoundError("Student not found")

    if request.method == "POST":  # Handle the update form submission
        try:
            # Validate the updated data
            data = StudentCreate(
                name=request.form.get("name"),
                email=request.form.get("email"),
                age=int(request.form.get("age")),
                course=request.form.get("course")
            )
            asyncio.run(update_student(id, data))  # Save updates to the DB
            flash("Student updated successfully!", "success")  # Show success flash message
            return redirect(url_for("students.index"))  # Go back to dashboard
        except ValueError as e:  # Handle validation errors
            raise ValidationError(f"Invalid input: {str(e)}")

    return render_template("edit_student.html", student=student)  # Show the edit form with student data


# --- API Routes (For JSON Data) ---

@student_bp.route("/api/students", methods=["POST"])  # API endpoint to create a student
def add_student_api():
    data = StudentCreate(**request.json)  # Parse JSON data from the request body
    student = asyncio.run(create_student(data))  # Create the student record
    return jsonify({"message": "Student created", "data": student.id})  # Return JSON response


@student_bp.route("/api/students", methods=["GET"])  # API endpoint to list all students
def get_all_students_api():
    students = asyncio.run(get_students())  # Fetch all students
    # Convert student objects to dictionaries for JSON serialization
    return jsonify([s.__dict__ for s in students if not s.__dict__.pop('_sa_instance_state', None)])


@student_bp.route("/api/students/<int:id>", methods=["PUT"])  # API endpoint to update a student
def update_api(id):
    data = StudentCreate(**request.json)  # Parse JSON updates
    student = asyncio.run(update_student(id, data))  # Update the record

    if not student:  # Return 404 if student not found
        raise ResourceNotFoundError("Student not found")

    return jsonify({"message": "Updated"})  # Return success message


@student_bp.route("/api/students/<int:id>", methods=["DELETE"])  # API endpoint to delete a student
def delete_api(id):
    student = asyncio.run(delete_student(id))  # Delete the record

    if not student:  # Return 404 if student doesn't exist
        raise ResourceNotFoundError("Student not found")

    return jsonify({"message": "Deleted"})  # Confirm deletion in JSON
