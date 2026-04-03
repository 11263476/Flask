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

@errors.app_errorhandler(Exception)  # Catch-all handler for any unhandled Python exceptions
def handle_unexpected_error(error):
    # Print the error to the server console help debugging
    print(f"CRITICAL ERROR: {str(error)}")
    
    if request.path.startswith('/api/'):
        return jsonify({"error": "An unexpected error occurred"}), 500
    
    # Render the pretty 500 error page for the user/examiner
    return render_template('errors/500.html'), 500
