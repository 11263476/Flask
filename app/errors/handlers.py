from flask import Blueprint, render_template, request, jsonify  # Flask utilities
from app.errors.exceptions import StudentAppError  # Our base exception class

errors = Blueprint('errors', __name__)  # Create a blueprint for error handling

@errors.app_errorhandler(StudentAppError)  # Global handler for our custom exceptions
def handle_student_app_error(error):
    # If the request is for the API, return a JSON error
    if request.path.startswith('/api/'):
        return jsonify(error.to_dict()), error.status_code
    # Otherwise, render an HTML error page (like 404.html or 400.html)
    return render_template(f'errors/{error.status_code}.html'), error.status_code

@errors.app_errorhandler(404)  # Handler for standard 404 Not Found errors
def error_404(error):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Not found"}), 404
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)  # Handler for standard 500 Internal Server errors
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
