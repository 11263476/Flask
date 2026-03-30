import os  # Import OS module to interact with environment variables
from datetime import timedelta  # Import timedelta for token expiration

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'viva-ready-secret-app-key'
    
    # --- JWT Security (Stateless Auth) ---
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'secure-student-jwt-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    
    # --- Cookie Security (Professional Setup) ---
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_SECURE = False  # Set to True ONLY in Production with HTTPS
    
    # --- CSRF Security (Conflict Resolution) ---
    # We disable JWT-level CSRF because we use the global Flask-WTF protection instead.
    JWT_COOKIE_CSRF_PROTECT = False 
