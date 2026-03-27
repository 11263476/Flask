from flask import Flask  # Import the core Flask class
from app.routes.student_routes import student_bp  # Import the student blueprint
from app.errors.handlers import errors  # Import the custom error handling blueprint
from app.config import Config  # Import the configuration class

def create_app():  # Define the Application Factory function
    app = Flask(__name__)  # Initialize the Flask instance
    app.config.from_object(Config)  # Load configurations from the Config class (like SECRET_KEY)
    
    app.register_blueprint(student_bp)  # Register the routes for student management
    app.register_blueprint(errors)  # Register the custom error handlers (404, 500, etc.)
    
    return app  # Return the fully configured app instance
