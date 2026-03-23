from flask import Flask
from app.routes.student_routes import student_bp
from app.errors.handlers import errors
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(student_bp)
    app.register_blueprint(errors)
    
    return app
