from flask import Blueprint, render_template, request, jsonify
from app.errors.exceptions import StudentAppError

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(StudentAppError)
def handle_student_app_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error.to_dict()), error.status_code
    return render_template(f'errors/{error.status_code}.html'), error.status_code

@errors.app_errorhandler(404)
def error_404(error):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Not found"}), 404
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def error_500(error):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Internal server error"}), 500
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(Exception)
def handle_unexpected_error(error):
    # Log the error here in a real app
    if request.path.startswith('/api/'):
        return jsonify({"error": "An unexpected error occurred"}), 500
    return render_template('errors/500.html'), 500
