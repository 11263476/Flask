from flask import Flask, redirect, url_for, flash  # Flask core
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity  # JWT support
from app.routes.student_routes import student_bp  # Student routes
from app.routes.auth_routes import auth_bp  # Auth routes
from app.errors.handlers import errors  # Error handlers
from app.config import Config  # Config settings

def create_app():
    app = Flask(__name__)  # Initialize app
    app.config.from_object(Config)  # Load settings
    
    # --- Initialize Extensions ---
    jwt = JWTManager(app) # Enable JWT
    
    # --- Global Context Processor ---
    # This function provides 'is_logged_in' and 'is_admin' to EVERY template automatically.
    # This prevents those pesky 500 errors if a variable is missing in index.html or base.html.
    @app.context_processor
    def inject_auth_status():
        try:
            token = get_jwt()
            return {
                "is_logged_in": get_jwt_identity() is not None,
                "is_admin": token.get("role") == "admin" if token else False
            }
        except:
            return {"is_logged_in": False, "is_admin": False}

    # --- JWT Redirect Handlers ---
    @jwt.unauthorized_loader
    def custom_unauthorized_response(_err):
        return redirect(url_for('auth.login'))

    @jwt.expired_token_loader
    def custom_expired_token_response(_headers, _payload):
        flash("Your session has expired. Please login again.", "warning")
        return redirect(url_for('auth.login'))
        
    @jwt.invalid_token_loader
    def custom_invalid_token_response(_err):
        response = redirect(url_for('auth.login'))
        from flask_jwt_extended import unset_jwt_cookies
        unset_jwt_cookies(response)
        flash("Invalid session. Please login again.", "danger")
        return response
    
    # --- Register Blueprints ---
    app.register_blueprint(student_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(errors)
    
    return app
