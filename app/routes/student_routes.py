from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, Response  # Flask utilities
import asyncio  # Asynchronous support
import csv, io # Data export utilities
from functools import wraps # For custom decorators
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity # JWT security

from app.errors.exceptions import ResourceNotFoundError, ValidationError # Our custom errors
from app.schemas.student_schema import StudentCreate # The data validation schema
from app.services.student_service import ( # Our database logic functions
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student,
    get_student_stats,
    search_students
)

# --- Security Decorator: Only allows users with role='admin' to proceed ---
def admin_required(f):
    @wraps(f)
    @jwt_required() # First, confirm they are logged in
    def decorated_function(*args, **kwargs):
        claims = get_jwt() # Get the token's extra information (like role)
        if claims.get("role") != "admin":
            flash("Error: You do not have permission to perform this action.", "danger")
            return redirect(url_for("students.index")) # Send them back to dashboard
        return f(*args, **kwargs)
    return decorated_function

student_bp = Blueprint("students", __name__) # Our student routes blueprint

# --- UI Routes (For Browser) ---

@student_bp.route("/")
@jwt_required() # REQUIRED login. If not logged in, user will be redirected to Login page.
def index():
    query = request.args.get("q")
    
    if query:
        students = asyncio.run(search_students(query))
    else:
        students = asyncio.run(get_students())
        
    stats = asyncio.run(get_student_stats())
    
    # We no longer need to check is_admin here manually! 
    # Our new context_processor in main.py handles it for the whole app.
    
    return render_template("index.html", students=students, stats=stats, query=query)


@student_bp.route("/export/csv")
@jwt_required() # Only logged-in users can export data
def export_csv():
    students = asyncio.run(get_students())
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Email", "Age", "Course", "Created At"])
    for s in students:
        writer.writerow([s.id, s.name, s.email, s.age, s.course, s.created_at.strftime('%Y-%m-%d %H:%M')])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=students_export.csv"}
    )


@student_bp.route("/student/<int:id>")
@jwt_required() # Require login to view specific profiles
def view_student(id):
    student = asyncio.run(get_student(id))
    if not student:
        raise ResourceNotFoundError("Student not found")
    
    token = get_jwt()
    is_admin = token.get("role") == "admin"
    return render_template("view_student.html", student=student, is_admin=is_admin)


@student_bp.route("/add", methods=["GET", "POST"])
@jwt_required() # Only logged-in users can access the add form
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
@jwt_required() # Only logged-in users can edit records
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


# --- API Routes (For JSON Data) ---

@student_bp.route("/api/students", methods=["POST"])
@jwt_required()
def add_student_api():
    data = StudentCreate(**request.json)
    student = asyncio.run(create_student(data))
    return jsonify({"message": "Student created", "data": student.id})


@student_bp.route("/api/students", methods=["GET"])
@jwt_required()
def get_all_students_api():
    students = asyncio.run(get_students())
    return jsonify([s.__dict__ for s in students if not s.__dict__.pop('_sa_instance_state', None)])


@student_bp.route("/api/students/<int:id>", methods=["PUT"])
@jwt_required()
def update_api(id):
    data = StudentCreate(**request.json)
    student = asyncio.run(update_student(id, data))
    if not student:
        raise ResourceNotFoundError("Student not found")
    return jsonify({"message": "Updated"})


@student_bp.route("/api/students/<int:id>", methods=["DELETE"])
@admin_required # Strictly only Admins can delete
def delete_api(id):
    student = asyncio.run(delete_student(id))
    if not student:
        raise ResourceNotFoundError("Student not found")
    return jsonify({"message": "Deleted"})
