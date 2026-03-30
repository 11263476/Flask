import os  # Import OS module to interact with environment variables
from datetime import timedelta  # Import timedelta for token expiration

class Config:  # Define a class to hold application configurations
    # Set the secret key for sessions, defaulting to a fallback string if not in environment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # --- JWT Configuration: Settings for token-based security ---
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-jwt-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Tokens last for 1 hour
    
    # Store JWT in cookies for professional browser integration
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_SECURE = False  # Set to True in production (HTTPS)
    JWT_COOKIE_CSRF_PROTECT = True # Now enabled for full security!
    JWT_CSRF_IN_COOKIES = True # Send the CSRF token as a separate cookie
