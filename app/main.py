from flask import Flask, redirect, url_for, flash
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity
from flask_wtf.csrf import CSRFProtect
from app.routes.student_routes import student_bp
from app.routes.auth_routes import auth_bp
from app.errors.handlers import errors
from app.config import Config

def create_app():
    app = Flask(__name__)  # Initialize app
    app.config.from_object(Config)
    
    jwt = JWTManager(app)
    csrf = CSRFProtect(app)
    
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
    
    app.register_blueprint(student_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(errors)
    
    return app
